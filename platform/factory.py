"""平台工厂模块，根据操作系统返回对应的平台实现"""
import sys


class Platform:
    """平台实例，聚合所有平台相关接口"""

    def __init__(self, serial, config, clipboard, filesystem, ui):
        self.serial = serial
        self.config = config
        self.clipboard = clipboard
        self.filesystem = filesystem
        self.ui = ui


def get_platform() -> Platform:
    """获取当前操作系统对应的平台实例

    Returns:
        Platform: 平台实例，包含serial、config、clipboard、filesystem、ui接口

    Raises:
        RuntimeError: 不支持的操作系统
    """
    # 使用sys.platform来判断操作系统，避免与本地platform包冲突
    if sys.platform.startswith('win'):
        system = "Windows"
    elif sys.platform.startswith('linux'):
        system = "Linux"
    elif sys.platform == 'darwin':
        system = "Darwin"
    else:
        system = "Unknown"

    if system == "Windows":
        from platform.windows import (
            WindowsSerial,
            WindowsConfig,
            WindowsClipboard,
            WindowsFilesystem,
            WindowsUI
        )
        return Platform(
            serial=WindowsSerial(),
            config=WindowsConfig(),
            clipboard=WindowsClipboard(),
            filesystem=WindowsFilesystem(),
            ui=WindowsUI()
        )

    elif system == "Linux":
        from platform.linux import (
            LinuxSerial,
            LinuxConfig,
            LinuxClipboard,
            LinuxFilesystem,
            LinuxUI
        )
        return Platform(
            serial=LinuxSerial(),
            config=LinuxConfig(),
            clipboard=LinuxClipboard(),
            filesystem=LinuxFilesystem(),
            ui=LinuxUI()
        )

    elif system == "Darwin":
        from platform.macos import (
            MacOSSerial,
            MacOSConfig,
            MacOSClipboard,
            MacOSFilesystem,
            MacOSUI
        )
        return Platform(
            serial=MacOSSerial(),
            config=MacOSConfig(),
            clipboard=MacOSClipboard(),
            filesystem=MacOSFilesystem(),
            ui=MacOSUI()
        )

    else:
        raise RuntimeError(f"Unsupported operating system: {system}")
