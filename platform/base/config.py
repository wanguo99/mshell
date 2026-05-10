"""配置路径接口基类"""
from abc import ABC, abstractmethod
from pathlib import Path


class ConfigBase(ABC):
    """配置路径管理的抽象基类，定义跨平台配置目录接口"""

    @abstractmethod
    def get_config_dir(self) -> Path:
        """获取配置文件目录

        Returns:
            Path: 配置目录路径
                Windows: %APPDATA%\MShell
                Linux: ~/.config/mshell
                macOS: ~/Library/Application Support/MShell
        """
        pass

    @abstractmethod
    def get_data_dir(self) -> Path:
        """获取数据文件目录

        Returns:
            Path: 数据目录路径，用于存储会话日志、历史记录等
        """
        pass

    @abstractmethod
    def get_cache_dir(self) -> Path:
        """获取缓存目录

        Returns:
            Path: 缓存目录路径，用于存储临时文件
        """
        pass
