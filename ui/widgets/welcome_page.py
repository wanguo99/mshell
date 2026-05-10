"""欢迎页面组件"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class WelcomePage(QWidget):
    """欢迎页面"""

    def __init__(self, platform_info=None, parent=None):
        super().__init__(parent)
        self.platform_info = platform_info
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;
            }
        """)
        self._init_ui()

    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.addStretch(2)

        # 标题
        title = QLabel("MShell")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #cccccc; background-color: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 副标题
        subtitle = QLabel("跨平台终端工具")
        subtitle.setStyleSheet("font-size: 16px; color: #aaaaaa; background-color: transparent; margin-top: 10px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        # 提示信息
        info = QLabel(
            "从左侧边栏选择已保存的会话\n"
            "或点击底部按钮创建新连接"
        )
        info.setStyleSheet("font-size: 14px; color: #888888; background-color: transparent; line-height: 1.6;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        layout.addStretch(3)
