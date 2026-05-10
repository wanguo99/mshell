"""Windows平台文件系统实现"""
import os
import subprocess
from pathlib import Path
from platform.base.filesystem import FilesystemBase


class WindowsFilesystem(FilesystemBase):
    """Windows平台文件系统操作实现"""

    def normalize_path(self, path: str) -> str:
        """规范化Windows路径，使用反斜杠"""
        return os.path.normpath(path)

    def open_file_manager(self, path: str) -> None:
        """在Windows资源管理器中打开路径"""
        try:
            normalized_path = self.normalize_path(path)
            if os.path.isfile(normalized_path):
                subprocess.run(['explorer', '/select,', normalized_path], check=False)
            else:
                subprocess.run(['explorer', normalized_path], check=False)
        except Exception:
            pass

    def get_home_dir(self) -> Path:
        """获取Windows用户主目录"""
        return Path.home()

    def get_path_separator(self) -> str:
        """获取Windows路径分隔符"""
        return "\\"
