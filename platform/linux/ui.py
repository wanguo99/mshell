"""Linux平台UI实现"""
from typing import List, Tuple
from platform.base.ui import UIBase


class LinuxUI(UIBase):
    """Linux平台UI相关操作实现"""

    def get_default_font(self) -> Tuple[str, int]:
        """获取Linux默认等宽字体"""
        return ("Monospace", 10)

    def get_available_fonts(self) -> List[str]:
        """获取Linux可用等宽字体列表"""
        return [
            "Monospace",
            "DejaVu Sans Mono",
            "Liberation Mono",
            "Ubuntu Mono",
            "Courier New",
        ]

    def get_shortcut_modifier(self) -> str:
        """获取Linux快捷键修饰符"""
        return "Ctrl"

    def get_line_ending(self) -> str:
        """获取Linux行尾符"""
        return "\n"

    def get_theme(self) -> str:
        """获取Linux系统主题"""
        try:
            import subprocess
            result = subprocess.run(
                ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'],
                capture_output=True,
                text=True,
                timeout=1
            )
            theme = result.stdout.strip().strip("'")
            return "dark" if "dark" in theme.lower() else "light"
        except Exception:
            return "light"
