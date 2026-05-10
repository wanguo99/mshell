"""串口连接管理

基于pyserial实现串口连接。
"""

import threading
import time
from typing import Optional

import serial
import serial.tools.list_ports

from core.connection_manager import ConnectionManager
from mshell_platform import get_platform


class SerialConnection(ConnectionManager):
    """串口连接管理器"""

    def __init__(self):
        super().__init__()
        self._serial: Optional[serial.Serial] = None
        self._receive_thread: Optional[threading.Thread] = None
        self._running = False
        self._disconnecting = False  # 防止重复断开通知
        self.platform = get_platform()

    def connect(self, port: str, baudrate: int = 9600, bytesize: int = 8,
                parity: str = 'N', stopbits: int = 1, timeout: float = 1.0) -> bool:
        """建立串口连接

        Args:
            port: 串口名称 (如 COM1, /dev/ttyUSB0)
            baudrate: 波特率
            bytesize: 数据位 (5, 6, 7, 8)
            parity: 校验位 ('N'=无, 'E'=偶, 'O'=奇, 'M'=标记, 'S'=空格)
            stopbits: 停止位 (1, 1.5, 2)
            timeout: 读取超时时间（秒）

        Returns:
            连接是否成功
        """
        try:
            # 转换校验位参数
            parity_map = {
                'N': serial.PARITY_NONE,
                'E': serial.PARITY_EVEN,
                'O': serial.PARITY_ODD,
                'M': serial.PARITY_MARK,
                'S': serial.PARITY_SPACE,
            }
            parity_value = parity_map.get(parity.upper(), serial.PARITY_NONE)

            # 转换停止位参数
            stopbits_map = {
                1: serial.STOPBITS_ONE,
                1.5: serial.STOPBITS_ONE_POINT_FIVE,
                2: serial.STOPBITS_TWO,
            }
            stopbits_value = stopbits_map.get(stopbits, serial.STOPBITS_ONE)

            # 创建串口对象
            self._serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity_value,
                stopbits=stopbits_value,
                timeout=timeout,
                write_timeout=timeout
            )

            # 启动接收线程
            self._running = True
            self._receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self._receive_thread.start()

            # 通知连接成功
            self._notify_connection_changed(True)

            return True

        except Exception as e:
            print(f"Serial connection failed: {e}")
            self._cleanup()
            return False

    def disconnect(self):
        """断开串口连接"""
        # 防止重复断开
        if self._disconnecting:
            return

        self._disconnecting = True
        self._running = False

        # 等待接收线程结束
        if self._receive_thread and self._receive_thread.is_alive():
            self._receive_thread.join(timeout=2)

        # 清理资源
        self._cleanup()

        # 通知连接断开
        self._notify_connection_changed(False)

    def send(self, data: bytes):
        """发送数据到串口

        Args:
            data: 要发送的字节数据
        """
        if not self.is_connected():
            return

        try:
            self._serial.write(data)
            self._serial.flush()
        except Exception as e:
            print(f"Serial send failed: {e}")
            self.disconnect()

    def is_connected(self) -> bool:
        """检查串口是否已连接

        Returns:
            是否已连接
        """
        return self._serial is not None and self._serial.is_open

    def _receive_loop(self):
        """接收数据循环（在独立线程中运行）"""
        while self._running and self.is_connected():
            try:
                if self._serial.in_waiting > 0:
                    data = self._serial.read(self._serial.in_waiting)
                    if data:
                        self._notify_data_received(data)
                else:
                    # 短暂休眠避免CPU占用过高
                    time.sleep(0.01)

            except Exception as e:
                print(f"Serial receive error: {e}")
                break

        # 接收循环结束，断开连接
        if self._running:
            self.disconnect()

    def _cleanup(self):
        """清理资源"""
        if self._serial:
            try:
                if self._serial.is_open:
                    self._serial.close()
            except Exception:
                pass
            self._serial = None

    @staticmethod
    def list_available_ports():
        """列出可用的串口

        Returns:
            串口信息列表
        """
        ports = []
        for port_info in serial.tools.list_ports.comports():
            ports.append({
                'device': port_info.device,
                'description': port_info.description,
                'hwid': port_info.hwid
            })
        return ports
