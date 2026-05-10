"""终端颜色方案

定义不同的终端颜色方案，包括default、solarized_dark、monokai等。
"""

from typing import Dict, Tuple


class ColorScheme:
    """颜色方案基类"""

    def __init__(self, name: str):
        self.name = name
        self.background: Tuple[int, int, int] = (0, 0, 0)
        self.foreground: Tuple[int, int, int] = (255, 255, 255)
        self.cursor: Tuple[int, int, int] = (255, 255, 255)
        self.selection: Tuple[int, int, int] = (100, 100, 100)

    def get_background(self) -> Tuple[int, int, int]:
        """获取背景色"""
        return self.background

    def get_foreground(self) -> Tuple[int, int, int]:
        """获取前景色"""
        return self.foreground

    def get_cursor(self) -> Tuple[int, int, int]:
        """获取光标颜色"""
        return self.cursor

    def get_selection(self) -> Tuple[int, int, int]:
        """获取选中文本背景色"""
        return self.selection


class DefaultColorScheme(ColorScheme):
    """默认颜色方案 (黑底白字)"""

    def __init__(self):
        super().__init__("default")
        self.background = (0, 0, 0)
        self.foreground = (229, 229, 229)
        self.cursor = (255, 255, 255)
        self.selection = (70, 70, 70)


class SolarizedDarkColorScheme(ColorScheme):
    """Solarized Dark颜色方案"""

    def __init__(self):
        super().__init__("solarized_dark")
        self.background = (0, 43, 54)      # base03
        self.foreground = (131, 148, 150)  # base0
        self.cursor = (147, 161, 161)      # base1
        self.selection = (7, 54, 66)       # base02


class MonokaiColorScheme(ColorScheme):
    """Monokai颜色方案"""

    def __init__(self):
        super().__init__("monokai")
        self.background = (39, 40, 34)
        self.foreground = (248, 248, 242)
        self.cursor = (253, 151, 31)
        self.selection = (73, 72, 62)


class DraculaColorScheme(ColorScheme):
    """Dracula颜色方案"""

    def __init__(self):
        super().__init__("dracula")
        self.background = (40, 42, 54)
        self.foreground = (248, 248, 242)
        self.cursor = (255, 255, 255)
        self.selection = (68, 71, 90)


class ColorSchemeManager:
    """颜色方案管理器"""

    def __init__(self):
        self._schemes: Dict[str, ColorScheme] = {
            "default": DefaultColorScheme(),
            "solarized_dark": SolarizedDarkColorScheme(),
            "monokai": MonokaiColorScheme(),
            "dracula": DraculaColorScheme(),
        }
        self._current_scheme = "default"

    def get_scheme(self, name: str) -> ColorScheme:
        """获取指定颜色方案

        Args:
            name: 方案名称

        Returns:
            颜色方案对象

        Raises:
            KeyError: 方案不存在
        """
        if name not in self._schemes:
            raise KeyError(f"Color scheme '{name}' not found")
        return self._schemes[name]

    def get_current_scheme(self) -> ColorScheme:
        """获取当前颜色方案

        Returns:
            当前颜色方案对象
        """
        return self._schemes[self._current_scheme]

    def set_current_scheme(self, name: str):
        """设置当前颜色方案

        Args:
            name: 方案名称

        Raises:
            KeyError: 方案不存在
        """
        if name not in self._schemes:
            raise KeyError(f"Color scheme '{name}' not found")
        self._current_scheme = name

    def list_schemes(self) -> list:
        """列出所有可用的颜色方案

        Returns:
            方案名称列表
        """
        return list(self._schemes.keys())

    def add_scheme(self, scheme: ColorScheme):
        """添加自定义颜色方案

        Args:
            scheme: 颜色方案对象
        """
        self._schemes[scheme.name] = scheme
