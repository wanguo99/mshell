"""会话实体 - 纯领域对象"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class SessionState(Enum):
    """会话状态"""
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class SessionEntity:
    """会话实体（纯领域对象，无业务逻辑）

    职责：
    - 封装会话的静态配置和动态状态
    - 不包含业务逻辑（连接、断开等由应用层处理）
    - 不依赖外部框架（如 PyQt）
    """

    # 静态配置
    session_id: str
    connection_type: str  # 'ssh', 'serial', 'telnet', 'local'
    name: str
    config: dict  # 连接配置（host, port, username等）

    # 动态状态
    state: SessionState = SessionState.CONNECTING
    created_at: datetime = field(default_factory=datetime.now)
    connected_at: Optional[datetime] = None
    disconnected_at: Optional[datetime] = None
    last_activity_at: datetime = field(default_factory=datetime.now)

    # 统计信息
    bytes_sent: int = 0
    bytes_received: int = 0
    error_message: Optional[str] = None

    def set_connected(self) -> None:
        """设置为已连接状态"""
        self.state = SessionState.CONNECTED
        self.connected_at = datetime.now()
        self.last_activity_at = datetime.now()

    def set_disconnected(self, error_message: Optional[str] = None) -> None:
        """设置为已断开状态"""
        if error_message:
            self.state = SessionState.ERROR
            self.error_message = error_message
        else:
            self.state = SessionState.DISCONNECTED
        self.disconnected_at = datetime.now()

    def update_activity(self) -> None:
        """更新最后活动时间"""
        self.last_activity_at = datetime.now()

    def record_sent(self, byte_count: int) -> None:
        """记录发送字节数"""
        self.bytes_sent += byte_count
        self.update_activity()

    def record_received(self, byte_count: int) -> None:
        """记录接收字节数"""
        self.bytes_received += byte_count
        self.update_activity()

    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self.state == SessionState.CONNECTED

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

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'session_id': self.session_id,
            'connection_type': self.connection_type,
            'name': self.name,
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
        return (f"SessionEntity(id={self.session_id[:8]}, name={self.name}, "
                f"state={self.state.value}, duration={self.duration}s)")
