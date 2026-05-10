"""事件类型定义"""

from dataclasses import dataclass
from typing import Optional
from .event_bus import Event


@dataclass
class SessionCreatedEvent(Event):
    """会话创建事件"""
    session_id: str
    connection_type: str  # 'ssh', 'serial', 'telnet'
    name: str


@dataclass
class SessionClosedEvent(Event):
    """会话关闭事件"""
    session_id: str
    reason: Optional[str] = None  # 关闭原因（正常关闭为None）


@dataclass
class DataReceivedEvent(Event):
    """数据接收事件"""
    session_id: str
    data: bytes


@dataclass
class DataSentEvent(Event):
    """数据发送事件"""
    session_id: str
    data: bytes


@dataclass
class ConnectionStateChangedEvent(Event):
    """连接状态变化事件"""
    session_id: str
    connected: bool
    error_message: Optional[str] = None


@dataclass
class TerminalResizeEvent(Event):
    """终端大小调整事件"""
    session_id: str
    rows: int
    cols: int


@dataclass
class TabCreateRequestEvent(Event):
    """标签页创建请求事件（应用层 -> UI层）"""
    session_id: str
    title: str


@dataclass
class TabCloseRequestEvent(Event):
    """标签页关闭请求事件（应用层 -> UI层）"""
    session_id: str
