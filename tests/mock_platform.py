# Mock Platform for Testing
# 用于开发阶段模拟platform模块

from typing import List, Tuple
from pathlib import Path


class MockSerial:
    """Mock串口接口"""

    def get_available_ports(self) -> List[str]:
        """返回模拟的串口列表"""
        return ["COM1", "COM2", "COM3", "/dev/ttyUSB0", "/dev/ttyUSB1"]

    def get_port_description(self, port: str) -> str:
        """返回串口描述"""
        return f"Mock Serial Port: {port}"


class MockConfig:
    """Mock配置接口"""

    def get_config_dir(self) -> Path:
        """返回配置目录"""
        return Path.home() / ".mshell"

    def get_data_dir(self) -> Path:
        """返回数据目录"""
        return Path.home() / ".mshell" / "data"

    def get_cache_dir(self) -> Path:
        """返回缓存目录"""
        return Path.home() / ".mshell" / "cache"


class MockClipboard:
    """Mock剪贴板接口"""

    def __init__(self):
        self._text = ""

    def get_text(self) -> str:
        """获取剪贴板文本"""
        return self._text

    def set_text(self, text: str):
        """设置剪贴板文本"""
        self._text = text


class MockFilesystem:
    """Mock文件系统接口"""

    def normalize_path(self, path: str) -> str:
        """规范化路径"""
        return path.replace("\\", "/")

    def get_home_dir(self) -> Path:
        """获取用户主目录"""
        return Path.home()

    def open_file_manager(self, path: str):
        """打开文件管理器"""
        print(f"[Mock] Opening file manager at: {path}")

    def get_path_separator(self) -> str:
        """获取路径分隔符"""
        return "/"


class MockUI:
    """Mock UI接口"""

    def get_default_font(self) -> Tuple[str, int]:
        """获取默认字体"""
        return ("Consolas", 12)

    def get_available_fonts(self) -> List[str]:
        """获取可用字体列表"""
        return ["Consolas", "Courier New", "Monospace", "Monaco"]

    def get_shortcut_modifier(self) -> str:
        """获取快捷键修饰符"""
        return "Ctrl"

    def get_line_ending(self) -> str:
        """获取行尾符"""
        return "\n"


class MockPlatform:
    """Mock平台聚合类"""

    def __init__(self):
        self.serial = MockSerial()
        self.config = MockConfig()
        self.clipboard = MockClipboard()
        self.filesystem = MockFilesystem()
        self.ui = MockUI()


def get_mock_platform() -> MockPlatform:
    """获取Mock平台实例"""
    return MockPlatform()
