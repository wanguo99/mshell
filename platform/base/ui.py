"""UI接口基类"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class UIBase(ABC):
    """UI相关操作的抽象基类，定义跨平台UI接口"""

    @abstractmethod
    def get_default_font(self) -> Tuple[str, int]:
        """获取默认等宽字体

        Returns:
            Tuple[str, int]: (字体名称, 字体大小)
                Windows: ("Consolas", 10)
                Linux: ("Monospace", 10)
                macOS: ("Menlo", 12)
        """
        pass

    @abstractmethod
    def get_available_fonts(self) -> List[str]:
        """获取系统可用的等宽字体列表

        Returns:
            List[str]: 等宽字体名称列表
        """
        pass

    @abstractmethod
    def get_shortcut_modifier(self) -> str:
        """获取快捷键修饰符

        Returns:
            str: 快捷键修饰符
                Windows/Linux: "Ctrl"
                macOS: "Cmd"
        """
        pass

    @abstractmethod
    def get_line_ending(self) -> str:
        """获取系统默认行尾符

        Returns:
            str: 行尾符
                Windows: "\\r\\n"
                Linux/macOS: "\\n"
        """
        pass

    @abstractmethod
    def get_theme(self) -> str:
        """获取系统主题

        Returns:
            str: 主题名称 ("light" 或 "dark")
        """
        pass
