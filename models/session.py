"""会话数据模型"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from models.connection import ConnectionConfig


class SessionState(Enum):
    """会话状态枚举"""
    CONNECTING = "connecting"      # 正在连接
    CONNECTED = "connected"        # 已连接
    DISCONNECTED = "disconnected"  # 已断开
    ERROR = "error"                # 错误状态


class Session:
    """会话模型，表示一个活动的连接会话

    封装了会话的所有状态和行为，包括：
    - 静态配置：连接配置、会话ID
    - 动态属性：连接状态、创建时间、最后活动时间
    - 关联对象：连接对象、终端widget
    - 会话行为：连接、断开、发送数据
    """

    def __init__(self, config: ConnectionConfig, connection, terminal):
        """初始化会话

        Args:
            config: 连接配置
            connection: 连接对象（SSHConnection或SerialConnection）
            terminal: 终端widget
        """
        # === 静态配置 ===
        self.session_id = str(uuid.uuid4())  # 会话唯一ID
        self.config = config                  # 连接配置

        # === 关联对象 ===
        self.connection = connection          # 连接对象
        self.terminal = terminal              # 终端widget

        # === 动态属性 ===
        self.state = SessionState.CONNECTING  # 会话状态
        self.created_at = datetime.now()      # 创建时间
        self.connected_at: Optional[datetime] = None  # 连接时间
        self.disconnected_at: Optional[datetime] = None  # 断开时间
        self.last_activity_at = datetime.now()  # 最后活动时间

        # === 会话统计 ===
        self.bytes_sent = 0                   # 发送字节数
        self.bytes_received = 0               # 接收字节数
        self.error_message: Optional[str] = None  # 错误信息

        # === UI相关 ===
        self.tab_index: Optional[int] = None  # 标签页索引（由外部设置）
        self.tab_name = config.name           # 标签页名称

    @property
    def connection_id(self) -> str:
        """连接配置ID"""
        return self.config.id

    @property
    def display_name(self) -> str:
        """显示名称"""
        return self.tab_name

    @property
    def duration(self) -> Optional[float]:
        """会话持续时间（秒）"""
        if self.connected_at:
            end_time = self.disconnected_at or datetime.now()
            return (end_time - self.connected_at).total_seconds()
        return None

    @property
    def idle_time(self) -> float:
        """空闲时间（秒）"""
        return (datetime.now() - self.last_activity_at).total_seconds()

    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self.state == SessionState.CONNECTED and self.connection.is_connected()

    def set_connected(self):
        """设置为已连接状态"""
        self.state = SessionState.CONNECTED
        self.connected_at = datetime.now()
        self.last_activity_at = datetime.now()

    def set_disconnected(self, error_message: Optional[str] = None):
        """设置为已断开状态

        Args:
            error_message: 错误信息（如果是异常断开）
        """
        if error_message:
            self.state = SessionState.ERROR
            self.error_message = error_message
        else:
            self.state = SessionState.DISCONNECTED

        self.disconnected_at = datetime.now()

    def disconnect(self):
        """断开连接"""
        if self.connection and self.is_connected():
            self.connection.disconnect()
            self.set_disconnected()

    def send(self, data: bytes):
        """发送数据

        Args:
            data: 要发送的数据
        """
        if self.connection and self.is_connected():
            self.connection.send(data)
            self.bytes_sent += len(data)
            self.last_activity_at = datetime.now()

    def on_data_received(self, data: bytes):
        """接收数据回调

        Args:
            data: 接收到的数据
        """
        self.bytes_received += len(data)
        self.last_activity_at = datetime.now()

    def get_statistics(self) -> Dict[str, Any]:
        """获取会话统计信息

        Returns:
            统计信息字典
        """
        return {
            'session_id': self.session_id,
            'connection_id': self.connection_id,
            'name': self.display_name,
            'state': self.state.value,
            'created_at': self.created_at.isoformat(),
            'connected_at': self.connected_at.isoformat() if self.connected_at else None,
            'disconnected_at': self.disconnected_at.isoformat() if self.disconnected_at else None,
            'duration': self.duration,
            'idle_time': self.idle_time,
            'bytes_sent': self.bytes_sent,
            'bytes_received': self.bytes_received,
            'error_message': self.error_message
        }

    def __repr__(self):
        return (f"Session(id={self.session_id[:8]}, name={self.tab_name}, "
                f"state={self.state.value}, duration={self.duration}s)")

    def __str__(self):
        return f"{self.display_name} ({self.state.value})"
