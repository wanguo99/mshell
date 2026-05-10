"""连接管理抽象基类

定义连接管理器的统一接口，供SSH和串口连接实现。
"""

from abc import ABC, abstractmethod
from typing import Callable, Optional


class ConnectionManager(ABC):
    """连接管理器抽象基类"""

    def __init__(self):
        # 数据接收回调: (data: bytes) -> None
        self.on_data_received: Optional[Callable[[bytes], None]] = None
        # 连接状态变化回调: (connected: bool) -> None
        self.on_connection_changed: Optional[Callable[[bool], None]] = None

    @abstractmethod
    def connect(self, **kwargs) -> bool:
        """建立连接

        Args:
            **kwargs: 连接参数（由子类定义）

        Returns:
            连接是否成功
        """
        pass

    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass

    @abstractmethod
    def send(self, data: bytes):
        """发送数据

        Args:
            data: 要发送的字节数据
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """检查是否已连接

        Returns:
            是否已连接
        """
        pass

    def _notify_data_received(self, data: bytes):
        """通知数据接收

        Args:
            data: 接收到的数据
        """
        if self.on_data_received:
            self.on_data_received(data)

    def _notify_connection_changed(self, connected: bool):
        """通知连接状态变化

        Args:
            connected: 是否已连接
        """
        if self.on_connection_changed:
            self.on_connection_changed(connected)
