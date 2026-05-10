"""串口接口基类"""
from abc import ABC, abstractmethod
from typing import List


class SerialBase(ABC):
    """串口操作的抽象基类，定义跨平台串口接口"""

    @abstractmethod
    def get_available_ports(self) -> List[str]:
        """获取可用串口列表

        Returns:
            List[str]: 串口名称列表
                Windows: ["COM1", "COM2", "COM3"]
                Linux: ["/dev/ttyUSB0", "/dev/ttyACM0", "/dev/ttyS0"]
                macOS: ["/dev/tty.usbserial-*", "/dev/cu.usbserial-*"]
        """
        pass

    @abstractmethod
    def get_port_description(self, port: str) -> str:
        """获取串口描述信息

        Args:
            port: 串口名称

        Returns:
            str: 串口描述，如 "USB Serial Port (COM3)"
        """
        pass
