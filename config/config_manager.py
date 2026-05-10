"""配置管理模块"""
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from mshell_platform.factory import get_platform


class ConfigManager:
    """配置管理器，负责加载、保存和访问配置"""

    def __init__(self, config_file: Optional[str] = None):
        """初始化配置管理器

        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        self._platform = get_platform()
        if config_file:
            self._config_file = Path(config_file)
        else:
            self._config_file = self._platform.config.get_config_dir() / 'config.yaml'
        self._config: Dict[str, Any] = {}
        self._default_config_file = Path(__file__).parent / 'default_config.yaml'

    def load(self) -> None:
        """加载配置文件，如果不存在则使用默认配置"""
        if self._config_file.exists():
            with open(self._config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        else:
            self._load_default_config()
            self.save()

    def _load_default_config(self) -> None:
        """加载默认配置"""
        if self._default_config_file.exists():
            with open(self._default_config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        else:
            self._config = {}

    def save(self) -> None:
        """保存配置到文件"""
        self._config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._config_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self._config, f, allow_unicode=True, default_flow_style=False)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项

        Args:
            key: 配置键，支持点号分隔的嵌套键，如 "terminal.font_size"
            default: 默认值

        Returns:
            配置值，如果不存在则返回默认值
        """
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """设置配置项

        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
        """
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def get_connections(self) -> List[Dict[str, Any]]:
        """获取所有连接配置

        Returns:
            连接配置列表
        """
        return self.get('connections', [])

    def add_connection(self, connection: Dict[str, Any]) -> None:
        """添加连接配置

        Args:
            connection: 连接配置字典
        """
        connections = self.get_connections()
        connections.append(connection)
        self.set('connections', connections)

    def remove_connection(self, name: str) -> bool:
        """删除连接配置

        Args:
            name: 连接名称

        Returns:
            是否删除成功
        """
        connections = self.get_connections()
        for i, conn in enumerate(connections):
            if conn.get('name') == name:
                connections.pop(i)
                self.set('connections', connections)
                return True
        return False

    def get_shortcuts(self) -> Dict[str, str]:
        """获取快捷键配置

        Returns:
            快捷键配置字典
        """
        return self.get('shortcuts', {})

    def set_shortcut(self, key: str, action: str) -> None:
        """设置快捷键

        Args:
            key: 快捷键组合，如 "Ctrl+T"
            action: 动作名称
        """
        shortcuts = self.get_shortcuts()
        shortcuts[key] = action
        self.set('shortcuts', shortcuts)

    def get_quick_commands(self) -> List[Dict[str, str]]:
        """获取快捷指令配置

        Returns:
            快捷指令列表
        """
        return self.get('quick_commands', [])

    def add_quick_command(self, command: Dict[str, str]) -> None:
        """添加快捷指令

        Args:
            command: 快捷指令字典，包含name、command、shortcut
        """
        commands = self.get_quick_commands()
        commands.append(command)
        self.set('quick_commands', commands)

    def get_terminal_settings(self) -> Dict[str, Any]:
        """获取终端设置

        Returns:
            终端设置字典
        """
        return self.get('terminal', {})

    def get_color_schemes(self) -> Dict[str, Dict[str, Any]]:
        """获取所有颜色方案

        Returns:
            颜色方案字典
        """
        return self.get('color_schemes', {})

    def get_color_scheme(self, name: str) -> Optional[Dict[str, Any]]:
        """获取指定颜色方案

        Args:
            name: 颜色方案名称

        Returns:
            颜色方案配置，如果不存在则返回None
        """
        schemes = self.get_color_schemes()
        return schemes.get(name)
