"""Connection Manager Base Class

Defines unified interface for connection managers (SSH and Serial).
"""

from abc import ABCMeta, abstractmethod
from PyQt5.QtCore import QObject, pyqtSignal


class QABCMeta(type(QObject), ABCMeta):
    """Metaclass compatible with both QObject and ABC"""
    pass


class ConnectionManager(QObject, metaclass=QABCMeta):
    """Connection Manager Abstract Base Class"""

    # Signal: data received
    data_received = pyqtSignal(bytes)
    # Signal: connection status changed
    connection_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    @abstractmethod
    def connect(self, **kwargs) -> bool:
        """Establish connection

        Args:
            **kwargs: Connection parameters (defined by subclass)

        Returns:
            Whether connection succeeded
        """
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect"""
        pass

    @abstractmethod
    def send(self, data: bytes):
        """Send data

        Args:
            data: Byte data to send
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connected

        Returns:
            Whether connected
        """
        pass

    def _notify_data_received(self, data: bytes):
        """Notify data received (thread-safe)

        Args:
            data: Received data
        """
        self.data_received.emit(data)

    def _notify_connection_changed(self, connected: bool):
        """Notify connection status changed (thread-safe)

        Args:
            connected: Whether connected
        """
        self.connection_changed.emit(connected)
