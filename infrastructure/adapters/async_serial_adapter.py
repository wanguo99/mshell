"""异步串口连接适配器（增强版）

使用 asyncio + pyserial 实现异步串口连接，支持完整的串口参数配置。
"""

import asyncio
import serial
import serial.tools.list_ports
from typing import AsyncIterator, Optional, List, Dict
from domain.connection.connection import IConnection


class AsyncSerialAdapter(IConnection):
    """异步串口连接适配器（增强版）

    支持完整的串口参数：波特率、数据位、校验位、停止位等。
    """

    def __init__(self):
        self._serial: Optional[serial.Serial] = None
        self._running = False
        self._port: Optional[str] = None

    @property
    def connection_type(self) -> str:
        return 'serial'

    async def connect(self, port: str, baudrate: int = 9600,
                     bytesize: int = 8, parity: str = 'N',
                     stopbits: float = 1, timeout: float = 1, **kwargs) -> bool:
        """异步建立串口连接

        Args:
            port: 串口设备路径 (如 /dev/ttyUSB0, COM1)
            baudrate: 波特率 (默认 9600)
            bytesize: 数据位 (5, 6, 7, 8，默认 8)
            parity: 校验位 ('N'=无, 'E'=偶, 'O'=奇, 'M'=标记, 'S'=空格，默认 'N')
            stopbits: 停止位 (1, 1.5, 2，默认 1)
            timeout: 读取超时时间（秒，默认 1.0）

        Returns:
            连接是否成功
        """
        try:
            # 在线程池中执行同步连接操作
            await asyncio.to_thread(self._connect_sync, port, baudrate,
                                   bytesize, parity, stopbits, timeout)
            self._running = True
            self._port = port
            return True

        except Exception as e:
            print(f"Serial connection failed: {e}")
            await self._cleanup()
            return False

    def _connect_sync(self, port: str, baudrate: int, bytesize: int,
                     parity: str, stopbits: float, timeout: float) -> None:
        """同步连接（在线程池中执行）"""
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

    async def disconnect(self) -> None:
        """异步断开连接"""
        self._running = False
        await self._cleanup()

    async def send(self, data: bytes) -> None:
        """异步发送数据

        Args:
            data: 要发送的字节数据
        """
        if not self.is_connected():
            return

        try:
            # 在线程池中执行同步发送
            await asyncio.to_thread(self._serial.write, data)
            await asyncio.to_thread(self._serial.flush)
        except Exception as e:
            print(f"Serial send failed: {e}")
            await self.disconnect()

    async def receive(self) -> AsyncIterator[bytes]:
        """异步接收数据（生成器）

        Yields:
            接收到的字节数据
        """
        while self._running and self.is_connected():
            try:
                # 在线程池中检查是否有数据
                in_waiting = await asyncio.to_thread(lambda: self._serial.in_waiting)

                if in_waiting > 0:
                    # 在线程池中接收数据
                    data = await asyncio.to_thread(self._serial.read, in_waiting)
                    if data:
                        yield data
                else:
                    # 短暂休眠避免 CPU 占用过高
                    await asyncio.sleep(0.01)

            except Exception as e:
                print(f"Serial receive error: {e}")
                break

        # 接收循环结束，断开连接
        if self._running:
            await self.disconnect()

    def is_connected(self) -> bool:
        """检查串口是否已连接

        Returns:
            是否已连接
        """
        return self._serial is not None and self._serial.is_open

    async def resize_terminal(self, rows: int, cols: int) -> None:
        """调整终端大小（串口不支持）

        Args:
            rows: 终端行数
            cols: 终端列数
        """
        # 串口连接不支持终端大小调整
        pass

    async def _cleanup(self) -> None:
        """清理资源"""
        if self._serial:
            try:
                await asyncio.to_thread(self._serial.close)
            except Exception:
                pass
            self._serial = None

    @staticmethod
    def list_available_ports() -> List[Dict[str, str]]:
        """列出可用的串口

        Returns:
            串口信息列表，每个元素包含 device, description, hwid
        """
        ports = []
        for port_info in serial.tools.list_ports.comports():
            ports.append({
                'device': port_info.device,
                'description': port_info.description,
                'hwid': port_info.hwid
            })
        return ports
