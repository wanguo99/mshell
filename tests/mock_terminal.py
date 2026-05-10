# Mock Terminal and Connection for Testing
# 用于开发阶段模拟terminal和core模块

from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtCore import pyqtSignal
from typing import Callable


class MockTerminalWidget(QWidget):
    """Mock终端组件"""

    data_to_send = pyqtSignal(bytes)

    def __init__(self, parent=None):
        super().__init__(parent)
        print("[Mock Terminal] Initialized")

    def write_output(self, data: str):
        """显示输出数据"""
        print(f"[Mock Terminal] Output: {data[:100]}...")

    def clear(self):
        """清空终端"""
        print("[Mock Terminal] Cleared")

    def set_color_scheme(self, scheme_name: str):
        """设置颜色方案"""
        print(f"[Mock Terminal] Color scheme: {scheme_name}")

    def set_font(self, font_family: str, font_size: int):
        """设置字体"""
        print(f"[Mock Terminal] Font: {font_family} {font_size}")


class MockConnectionManager:
    """Mock连接管理器"""

    def __init__(self):
        self.on_data_received: Callable[[bytes], None] = None
        self.on_connection_changed: Callable[[bool], None] = None
        self._connected = False
        print("[Mock Connection] Initialized")

    def connect(self, **kwargs) -> bool:
        """建立连接"""
        print(f"[Mock Connection] Connecting with: {kwargs}")
        self._connected = True
        if self.on_connection_changed:
            self.on_connection_changed(True)
        return True

    def disconnect(self):
        """断开连接"""
        print("[Mock Connection] Disconnecting")
        self._connected = False
        if self.on_connection_changed:
            self.on_connection_changed(False)

    def send(self, data: bytes):
        """发送数据"""
        print(f"[Mock Connection] Send: {data[:50]}...")
        # 模拟接收回显
        if self.on_data_received:
            self.on_data_received(data)

    def is_connected(self) -> bool:
        """检查连接状态"""
        return self._connected


class MockSSHConnection(MockConnectionManager):
    """Mock SSH连接"""

    def connect(self, host: str, port: int, username: str, password: str = None, key_file: str = None) -> bool:
        """SSH连接"""
        print(f"[Mock SSH] Connecting to {username}@{host}:{port}")
        return super().connect(host=host, port=port, username=username)


class MockSerialConnection(MockConnectionManager):
    """Mock串口连接"""

    def connect(self, port: str, baudrate: int, **kwargs) -> bool:
        """串口连接"""
        print(f"[Mock Serial] Connecting to {port} at {baudrate} baud")
        return super().connect(port=port, baudrate=baudrate)


class MockCommandExecutor:
    """Mock快捷指令执行器"""

    def __init__(self):
        self.commands = {}
        print("[Mock CommandExecutor] Initialized")

    def add_command(self, name: str, command: str):
        """添加快捷指令"""
        self.commands[name] = command
        print(f"[Mock CommandExecutor] Added command: {name} -> {command}")

    def execute(self, name: str, context: dict = None) -> str:
        """执行指令"""
        command = self.commands.get(name, "")
        print(f"[Mock CommandExecutor] Executing: {name} -> {command}")
        return command

    def get_all_commands(self) -> dict:
        """获取所有指令"""
        return self.commands.copy()
