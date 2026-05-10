"""剪贴板接口基类"""
from abc import ABC, abstractmethod


class ClipboardBase(ABC):
    """剪贴板操作的抽象基类，定义跨平台剪贴板接口"""

    @abstractmethod
    def get_text(self) -> str:
        """获取剪贴板文本内容

        Returns:
            str: 剪贴板中的文本，如果剪贴板为空或不包含文本则返回空字符串
        """
        pass

    @abstractmethod
    def set_text(self, text: str) -> None:
        """设置剪贴板文本内容

        Args:
            text: 要复制到剪贴板的文本
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """清空剪贴板内容"""
        pass
