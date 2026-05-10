"""macOS平台串口实现"""
import glob
from typing import List
from mshell_platform.base.serial import SerialBase


class MacOSSerial(SerialBase):
    """macOS平台串口操作实现"""

    def get_available_ports(self) -> List[str]:
        """获取macOS可用串口列表"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            return [port.device for port in ports]
        except ImportError:
            ports = []
            ports.extend(glob.glob('/dev/tty.usbserial-*'))
            ports.extend(glob.glob('/dev/cu.usbserial-*'))
            ports.extend(glob.glob('/dev/tty.usbmodem*'))
            ports.extend(glob.glob('/dev/cu.usbmodem*'))
            return sorted(ports)

    def get_port_description(self, port: str) -> str:
        """获取macOS串口描述信息"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            for p in ports:
                if p.device == port:
                    return p.description or f"Serial Port ({port})"
            return f"Serial Port ({port})"
        except ImportError:
            return f"Serial Port ({port})"
