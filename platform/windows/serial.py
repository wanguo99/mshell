"""Windows平台串口实现"""
from typing import List
from platform.base.serial import SerialBase


class WindowsSerial(SerialBase):
    """Windows平台串口操作实现"""

    def get_available_ports(self) -> List[str]:
        """获取Windows可用串口列表"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            return [port.device for port in ports]
        except ImportError:
            return []

    def get_port_description(self, port: str) -> str:
        """获取Windows串口描述信息"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            for p in ports:
                if p.device == port:
                    return p.description or f"Serial Port ({port})"
            return f"Serial Port ({port})"
        except ImportError:
            return f"Serial Port ({port})"
