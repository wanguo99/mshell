"""文件系统接口基类"""
from abc import ABC, abstractmethod
from pathlib import Path


class FilesystemBase(ABC):
    """文件系统操作的抽象基类，定义跨平台文件系统接口"""

    @abstractmethod
    def normalize_path(self, path: str) -> str:
        """规范化路径格式

        Args:
            path: 原始路径

        Returns:
            str: 规范化后的路径
                Windows: 使用反斜杠 \
                Linux/macOS: 使用正斜杠 /
        """
        pass

    @abstractmethod
    def open_file_manager(self, path: str) -> None:
        """在文件管理器中打开指定路径

        Args:
            path: 要打开的文件或目录路径
        """
        pass

    @abstractmethod
    def get_home_dir(self) -> Path:
        """获取用户主目录

        Returns:
            Path: 用户主目录路径
        """
        pass

    @abstractmethod
    def get_path_separator(self) -> str:
        """获取路径分隔符

        Returns:
            str: 路径分隔符
                Windows: "\\"
                Linux/macOS: "/"
        """
        pass
