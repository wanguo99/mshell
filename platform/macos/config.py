"""macOS平台配置路径实现"""
from pathlib import Path
from platform.base.config import ConfigBase


class MacOSConfig(ConfigBase):
    """macOS平台配置路径管理实现"""

    def get_config_dir(self) -> Path:
        """获取macOS配置目录: ~/Library/Application Support/MShell"""
        config_dir = Path.home() / 'Library' / 'Application Support' / 'MShell'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def get_data_dir(self) -> Path:
        """获取macOS数据目录"""
        data_dir = self.get_config_dir() / 'data'
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    def get_cache_dir(self) -> Path:
        """获取macOS缓存目录"""
        cache_dir = Path.home() / 'Library' / 'Caches' / 'MShell'
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
