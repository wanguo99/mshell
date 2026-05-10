"""macOS平台UI实现"""
from typing import List, Tuple
from platform.base.ui import UIBase


class MacOSUI(UIBase):
    """macOS平台UI相关操作实现"""

    def get_default_font(self) -> Tuple[str, int]:
        """获取macOS默认等宽字体"""
        return ("Menlo", 12)

    def get_available_fonts(self) -> List[str]:
        """获取macOS可用等宽字体列表"""
        return [
            "Menlo",
            "Monaco",
            "Courier New",
            "SF Mono",
            "Andale Mono",
        ]

    def get_shortcut_modifier(self) -> str:
        """获取macOS快捷键修饰符"""
        return "Cmd"

    def get_line_ending(self) -> str:
        """获取macOS行尾符"""
        return "\n"

    def get_theme(self) -> str:
        """获取macOS系统主题"""
        try:
            import subprocess
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                capture_output=True,
                text=True,
                timeout=1
            )
            return "dark" if result.returncode == 0 else "light"
        except Exception:
            return "light"
