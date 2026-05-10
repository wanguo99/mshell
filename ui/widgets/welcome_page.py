"""欢迎页面组件"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ui.theme import Theme


class WelcomePage(QWidget):
    """欢迎页面"""

    def __init__(self, platform_info=None, parent=None):
        super().__init__(parent)
        self.platform_info = platform_info
        self.setStyleSheet(f"QWidget {{ background-color: {Theme.TERMINAL_BG}; }}")
        self._init_ui()

    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.addStretch(2)

        # 标题
        title = QLabel("MShell")
        title.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {Theme.TEXT_HIGHLIGHT}; background-color: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 副标题
        subtitle = QLabel("跨平台终端工具")
        subtitle.setStyleSheet(f"font-size: 16px; color: {Theme.TEXT_PRIMARY}; background-color: transparent; margin-top: 10px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        # 提示信息
        info = QLabel(
            "从左侧边栏选择已保存的会话\n"
            "或点击底部按钮创建新连接"
        )
        info.setStyleSheet(f"font-size: 14px; color: {Theme.TEXT_SECONDARY}; background-color: transparent; line-height: 1.6;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        layout.addStretch(3)
