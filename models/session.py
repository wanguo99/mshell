"""会话数据模型"""

from typing import Optional
from models.connection import ConnectionConfig


class Session:
    """会话模型，表示一个活动的连接会话"""

    def __init__(self, tab_index: int, config: ConnectionConfig, connection, terminal):
        """初始化会话

        Args:
            tab_index: 标签页索引
            config: 连接配置
            connection: 连接对象（SSHConnection或SerialConnection）
            terminal: 终端widget
        """
        self.tab_index = tab_index
        self.config = config
        self.connection = connection
        self.terminal = terminal
        self.tab_name = config.name

    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self.connection.is_connected()

    def disconnect(self):
        """断开连接"""
        if self.connection:
            self.connection.disconnect()

    def send(self, data: bytes):
        """发送数据"""
        if self.connection:
            self.connection.send(data)

    def __repr__(self):
        return f"Session(tab_index={self.tab_index}, name={self.tab_name}, connected={self.is_connected()})"
