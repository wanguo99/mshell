"""Linux平台剪贴板实现"""
from platform.base.clipboard import ClipboardBase


class LinuxClipboard(ClipboardBase):
    """Linux平台剪贴板操作实现"""

    def get_text(self) -> str:
        """获取Linux剪贴板文本"""
        try:
            import pyperclip
            return pyperclip.paste() or ""
        except Exception:
            return ""

    def set_text(self, text: str) -> None:
        """设置Linux剪贴板文本"""
        try:
            import pyperclip
            pyperclip.copy(text)
        except Exception:
            pass

    def clear(self) -> None:
        """清空Linux剪贴板"""
        try:
            import pyperclip
            pyperclip.copy("")
        except Exception:
            pass
