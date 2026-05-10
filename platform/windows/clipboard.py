"""Windows平台剪贴板实现"""
from platform.base.clipboard import ClipboardBase


class WindowsClipboard(ClipboardBase):
    """Windows平台剪贴板操作实现"""

    def get_text(self) -> str:
        """获取Windows剪贴板文本"""
        try:
            import pyperclip
            return pyperclip.paste() or ""
        except Exception:
            return ""

    def set_text(self, text: str) -> None:
        """设置Windows剪贴板文本"""
        try:
            import pyperclip
            pyperclip.copy(text)
        except Exception:
            pass

    def clear(self) -> None:
        """清空Windows剪贴板"""
        try:
            import pyperclip
            pyperclip.copy("")
        except Exception:
            pass
