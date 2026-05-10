"""macOS平台文件系统实现"""
import os
import subprocess
from pathlib import Path
from mshell_platform.base.filesystem import FilesystemBase


class MacOSFilesystem(FilesystemBase):
    """macOS平台文件系统操作实现"""

    def normalize_path(self, path: str) -> str:
        """规范化macOS路径，使用正斜杠"""
        return os.path.normpath(path)

    def open_file_manager(self, path: str) -> None:
        """使用open命令在macOS Finder中打开路径"""
        try:
            normalized_path = self.normalize_path(path)
            subprocess.run(['open', normalized_path], check=False)
        except Exception:
            pass

    def get_home_dir(self) -> Path:
        """获取macOS用户主目录"""
        return Path.home()

    def get_path_separator(self) -> str:
        """获取macOS路径分隔符"""
        return "/"
