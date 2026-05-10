"""Windows平台UI实现"""
from typing import List, Tuple
from platform.base.ui import UIBase


class WindowsUI(UIBase):
    """Windows平台UI相关操作实现"""

    def get_default_font(self) -> Tuple[str, int]:
        """获取Windows默认等宽字体"""
        return ("Consolas", 10)

    def get_available_fonts(self) -> List[str]:
        """获取Windows可用等宽字体列表"""
        return [
            "Consolas",
            "Courier New",
            "Lucida Console",
            "Cascadia Code",
            "Cascadia Mono",
        ]

    def get_shortcut_modifier(self) -> str:
        """获取Windows快捷键修饰符"""
        return "Ctrl"

    def get_line_ending(self) -> str:
        """获取Windows行尾符"""
        return "\r\n"

    def get_theme(self) -> str:
        """获取Windows系统主题"""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return "light" if value == 1 else "dark"
        except Exception:
            return "light"
