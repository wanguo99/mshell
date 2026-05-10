"""SFTP客户端模块

提供基于SSH连接的SFTP文件传输功能
"""

import os
import stat
from typing import List, Dict, Callable, Optional
from pathlib import Path


class FileInfo:
    """文件信息"""

    def __init__(self, name: str, size: int, is_dir: bool, mtime: float, permissions: str):
        self.name = name
        self.size = size
        self.is_dir = is_dir
        self.mtime = mtime
        self.permissions = permissions


class SFTPClient:
    """SFTP客户端

    基于SSH连接提供文件传输功能
    """

    def __init__(self, ssh_connection):
        """初始化SFTP客户端

        Args:
            ssh_connection: SSH连接对象（需要有get_sftp_client()方法）
        """
        self.ssh_connection = ssh_connection
        self._sftp = None
        self._init_sftp()

    def _init_sftp(self):
        """初始化SFTP会话"""
        if not self.ssh_connection.is_connected():
            raise ConnectionError("SSH连接未建立")

        # 从SSH连接获取SFTP客户端
        if hasattr(self.ssh_connection, 'get_sftp_client'):
            self._sftp = self.ssh_connection.get_sftp_client()
        elif hasattr(self.ssh_connection, '_client'):
            # 如果SSH连接有paramiko客户端
            self._sftp = self.ssh_connection._client.open_sftp()
        else:
            raise AttributeError("SSH连接不支持SFTP")

    def upload(self, local_path: str, remote_path: str,
               progress_callback: Optional[Callable[[int], None]] = None) -> bool:
        """上传文件

        Args:
            local_path: 本地文件路径
            remote_path: 远程文件路径
            progress_callback: 进度回调函数，参数为百分比(0-100)

        Returns:
            是否成功
        """
        if not self._sftp:
            return False

        try:
            local_path = os.path.expanduser(local_path)
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"本地文件不存在: {local_path}")

            file_size = os.path.getsize(local_path)
            transferred = [0]

            def callback(sent, total):
                transferred[0] = sent
                if progress_callback and total > 0:
                    progress = int((sent / total) * 100)
                    progress_callback(progress)

            self._sftp.put(local_path, remote_path, callback=callback)
            return True

        except Exception as e:
            print(f"上传失败: {e}")
            return False

    def download(self, remote_path: str, local_path: str,
                 progress_callback: Optional[Callable[[int], None]] = None) -> bool:
        """下载文件

        Args:
            remote_path: 远程文件路径
            local_path: 本地文件路径
            progress_callback: 进度回调函数，参数为百分比(0-100)

        Returns:
            是否成功
        """
        if not self._sftp:
            return False

        try:
            local_path = os.path.expanduser(local_path)
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir)

            def callback(received, total):
                if progress_callback and total > 0:
                    progress = int((received / total) * 100)
                    progress_callback(progress)

            self._sftp.get(remote_path, local_path, callback=callback)
            return True

        except Exception as e:
            print(f"下载失败: {e}")
            return False

    def list_dir(self, remote_path: str = ".") -> List[FileInfo]:
        """列出目录内容

        Args:
            remote_path: 远程目录路径

        Returns:
            文件信息列表
        """
        if not self._sftp:
            return []

        try:
            files = []
            for attr in self._sftp.listdir_attr(remote_path):
                is_dir = stat.S_ISDIR(attr.st_mode)
                permissions = self._format_permissions(attr.st_mode)

                file_info = FileInfo(
                    name=attr.filename,
                    size=attr.st_size or 0,
                    is_dir=is_dir,
                    mtime=attr.st_mtime or 0,
                    permissions=permissions
                )
                files.append(file_info)

            return sorted(files, key=lambda f: (not f.is_dir, f.name.lower()))

        except Exception as e:
            print(f"列出目录失败: {e}")
            return []

    def remove(self, remote_path: str) -> bool:
        """删除文件

        Args:
            remote_path: 远程文件路径

        Returns:
            是否成功
        """
        if not self._sftp:
            return False

        try:
            self._sftp.remove(remote_path)
            return True
        except Exception as e:
            print(f"删除文件失败: {e}")
            return False

    def remove_dir(self, remote_path: str) -> bool:
        """删除目录

        Args:
            remote_path: 远程目录路径

        Returns:
            是否成功
        """
        if not self._sftp:
            return False

        try:
            self._sftp.rmdir(remote_path)
            return True
        except Exception as e:
            print(f"删除目录失败: {e}")
            return False

    def mkdir(self, remote_path: str) -> bool:
        """创建目录

        Args:
            remote_path: 远程目录路径

        Returns:
            是否成功
        """
        if not self._sftp:
            return False

        try:
            self._sftp.mkdir(remote_path)
            return True
        except Exception as e:
            print(f"创建目录失败: {e}")
            return False

    def rename(self, old_path: str, new_path: str) -> bool:
        """重命名文件或目录

        Args:
            old_path: 原路径
            new_path: 新路径

        Returns:
            是否成功
        """
        if not self._sftp:
            return False

        try:
            self._sftp.rename(old_path, new_path)
            return True
        except Exception as e:
            print(f"重命名失败: {e}")
            return False

    def get_cwd(self) -> str:
        """获取当前工作目录

        Returns:
            当前目录路径
        """
        if not self._sftp:
            return "/"

        try:
            return self._sftp.getcwd() or "/"
        except:
            return "/"

    def chdir(self, remote_path: str) -> bool:
        """切换工作目录

        Args:
            remote_path: 目标目录路径

        Returns:
            是否成功
        """
        if not self._sftp:
            return False

        try:
            self._sftp.chdir(remote_path)
            return True
        except Exception as e:
            print(f"切换目录失败: {e}")
            return False

    def stat(self, remote_path: str) -> Optional[FileInfo]:
        """获取文件信息

        Args:
            remote_path: 远程文件路径

        Returns:
            文件信息，失败返回None
        """
        if not self._sftp:
            return None

        try:
            attr = self._sftp.stat(remote_path)
            is_dir = stat.S_ISDIR(attr.st_mode)
            permissions = self._format_permissions(attr.st_mode)

            return FileInfo(
                name=os.path.basename(remote_path),
                size=attr.st_size or 0,
                is_dir=is_dir,
                mtime=attr.st_mtime or 0,
                permissions=permissions
            )
        except Exception as e:
            print(f"获取文件信息失败: {e}")
            return None

    def close(self):
        """关闭SFTP会话"""
        if self._sftp:
            try:
                self._sftp.close()
            except:
                pass
            self._sftp = None

    @staticmethod
    def _format_permissions(mode: int) -> str:
        """格式化权限字符串

        Args:
            mode: 文件模式

        Returns:
            权限字符串，如 "drwxr-xr-x"
        """
        is_dir = 'd' if stat.S_ISDIR(mode) else '-'

        perms = [
            'r' if mode & stat.S_IRUSR else '-',
            'w' if mode & stat.S_IWUSR else '-',
            'x' if mode & stat.S_IXUSR else '-',
            'r' if mode & stat.S_IRGRP else '-',
            'w' if mode & stat.S_IWGRP else '-',
            'x' if mode & stat.S_IXGRP else '-',
            'r' if mode & stat.S_IROTH else '-',
            'w' if mode & stat.S_IWOTH else '-',
            'x' if mode & stat.S_IXOTH else '-',
        ]

        return is_dir + ''.join(perms)
