"""连接接口 - 所有协议的统一抽象"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional


class IConnection(ABC):
    """连接接口（所有协议的统一抽象）

    所有连接类型（SSH、Serial、Telnet、LocalShell）都必须实现此接口。
    使用异步接口以统一处理 I/O 操作。
    """

    @abstractmethod
    async def connect(self, **kwargs) -> bool:
        """异步连接

        Args:
            **kwargs: 连接参数（不同协议参数不同）

        Returns:
            连接是否成功
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """异步断开连接"""
        pass

    @abstractmethod
    async def send(self, data: bytes) -> None:
        """异步发送数据

        Args:
            data: 要发送的字节数据
        """
        pass

    @abstractmethod
    async def receive(self) -> AsyncIterator[bytes]:
        """异步接收数据（生成器）

        Yields:
            接收到的字节数据
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """检查连接状态

        Returns:
            是否已连接
        """
        pass

    @abstractmethod
    async def resize_terminal(self, rows: int, cols: int) -> None:
        """调整终端大小

        Args:
            rows: 终端行数
            cols: 终端列数
        """
        pass

    @property
    @abstractmethod
    def connection_type(self) -> str:
        """连接类型标识

        Returns:
            'ssh', 'serial', 'telnet', 'local'
        """
        pass
