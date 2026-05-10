"""Connection Close Dialog

Dialog shown when a connection is closed, with option to remember choice.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QCheckBox)
from PyQt5.QtCore import Qt


class ConnectionCloseDialog(QDialog):
    """Dialog for connection close confirmation"""

    def __init__(self, connection_name, parent=None):
        super().__init__(parent)
        self.connection_name = connection_name
        self.remember_choice = False
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("连接已断开")
        self.setModal(True)
        self.setMinimumWidth(400)

        # 允许通过窗口关闭按钮关闭对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowCloseButtonHint)

        layout = QVBoxLayout(self)

        # Message
        message = QLabel(f"连接 '{self.connection_name}' 已断开")
        message.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(message)

        question = QLabel("是否关闭此标签页？")
        question.setStyleSheet("font-size: 12px; padding: 10px;")
        layout.addWidget(question)

        # Remember checkbox
        self.remember_checkbox = QCheckBox("记住我的选择，不再提示")
        self.remember_checkbox.setStyleSheet("padding: 10px;")
        layout.addWidget(self.remember_checkbox)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_yes = QPushButton("是")
        self.btn_yes.setMinimumWidth(80)
        self.btn_yes.clicked.connect(self.accept)
        button_layout.addWidget(self.btn_yes)

        self.btn_no = QPushButton("否")
        self.btn_no.setMinimumWidth(80)
        self.btn_no.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_no)

        layout.addLayout(button_layout)

    def accept(self):
        """Accept and remember choice if checked"""
        self.remember_choice = self.remember_checkbox.isChecked()
        super().accept()

    def reject(self):
        """Reject and remember choice if checked"""
        self.remember_choice = self.remember_checkbox.isChecked()
        super().reject()

    def closeEvent(self, event):
        """Handle window close button (X)"""
        # Treat close button as "No" (reject)
        self.remember_choice = self.remember_checkbox.isChecked()
        self.setResult(QDialog.Rejected)
        event.accept()
