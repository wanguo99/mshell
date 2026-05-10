"""Windows平台配置路径实现"""
import os
from pathlib import Path
from platform.base.config import ConfigBase


class WindowsConfig(ConfigBase):
    """Windows平台配置路径管理实现"""

    def get_config_dir(self) -> Path:
        """获取Windows配置目录: %APPDATA%\\MShell"""
        appdata = os.getenv('APPDATA')
        if not appdata:
            appdata = os.path.expanduser('~\\AppData\\Roaming')
        config_dir = Path(appdata) / 'MShell'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def get_data_dir(self) -> Path:
        """获取Windows数据目录"""
        data_dir = self.get_config_dir() / 'data'
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    def get_cache_dir(self) -> Path:
        """获取Windows缓存目录"""
        cache_dir = self.get_config_dir() / 'cache'
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
