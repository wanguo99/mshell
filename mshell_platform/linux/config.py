"""Linux平台配置路径实现"""
import os
from pathlib import Path
from mshell_platform.base.config import ConfigBase


class LinuxConfig(ConfigBase):
    """Linux平台配置路径管理实现，遵循XDG Base Directory规范"""

    def get_config_dir(self) -> Path:
        """获取Linux配置目录: ~/.config/mshell"""
        xdg_config = os.getenv('XDG_CONFIG_HOME')
        if xdg_config:
            config_dir = Path(xdg_config) / 'mshell'
        else:
            config_dir = Path.home() / '.config' / 'mshell'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def get_data_dir(self) -> Path:
        """获取Linux数据目录"""
        xdg_data = os.getenv('XDG_DATA_HOME')
        if xdg_data:
            data_dir = Path(xdg_data) / 'mshell'
        else:
            data_dir = Path.home() / '.local' / 'share' / 'mshell'
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    def get_cache_dir(self) -> Path:
        """获取Linux缓存目录"""
        xdg_cache = os.getenv('XDG_CACHE_HOME')
        if xdg_cache:
            cache_dir = Path(xdg_cache) / 'mshell'
        else:
            cache_dir = Path.home() / '.cache' / 'mshell'
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
