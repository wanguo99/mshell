"""连接配置数据模型"""

from typing import Optional, Dict, Any
from enum import Enum


class ConnectionType(Enum):
    """连接类型枚举"""
    SSH = "ssh"
    SERIAL = "serial"


class ConnectionConfig:
    """连接配置模型"""

    def __init__(self, config_dict: Dict[str, Any]):
        """初始化连接配置

        Args:
            config_dict: 配置字典
        """
        self.name = config_dict.get('name', 'Unnamed')
        self.type = ConnectionType(config_dict.get('type', 'ssh'))
        self._config = config_dict

    @property
    def config_dict(self) -> Dict[str, Any]:
        """获取原始配置字典"""
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)

    def __repr__(self):
        return f"ConnectionConfig(name={self.name}, type={self.type.value})"


class SSHConnectionConfig(ConnectionConfig):
    """SSH连接配置"""

    def __init__(self, config_dict: Dict[str, Any]):
        super().__init__(config_dict)
        self.host = config_dict.get('host', '')
        self.port = config_dict.get('port', 22)
        self.username = config_dict.get('username', '')
        self.password = config_dict.get('password', '')
        self.key_file = config_dict.get('key_file', '')

    @property
    def display_name(self) -> str:
        """显示名称"""
        return f"{self.name}\n{self.username}@{self.host}"


class SerialConnectionConfig(ConnectionConfig):
    """串口连接配置"""

    def __init__(self, config_dict: Dict[str, Any]):
        super().__init__(config_dict)
        self.port = config_dict.get('port', '')
        self.baudrate = config_dict.get('baudrate', 115200)
        self.bytesize = config_dict.get('bytesize', 8)
        self.parity = config_dict.get('parity', 'N')
        self.stopbits = config_dict.get('stopbits', 1)

    @property
    def display_name(self) -> str:
        """显示名称"""
        return f"{self.name}\n{self.port}"


def create_connection_config(config_dict: Dict[str, Any]) -> ConnectionConfig:
    """工厂方法：根据配置字典创建对应的连接配置对象

    Args:
        config_dict: 配置字典

    Returns:
        ConnectionConfig子类实例
    """
    conn_type = config_dict.get('type', 'ssh')

    if conn_type == 'ssh':
        return SSHConnectionConfig(config_dict)
    elif conn_type == 'serial':
        return SerialConnectionConfig(config_dict)
    else:
        return ConnectionConfig(config_dict)
