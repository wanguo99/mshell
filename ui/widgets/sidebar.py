"""侧边栏组件"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QListWidgetItem, QPushButton, QMenu)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor

from models.connection import ConnectionConfig


class Sidebar(QWidget):
    """侧边栏组件，显示会话列表和新建连接按钮"""

    # 信号定义
    connection_selected = pyqtSignal(ConnectionConfig)  # 双击连接项
    connection_edit = pyqtSignal(ConnectionConfig)  # 编辑连接
    connection_delete = pyqtSignal(str)  # 删除连接（传递连接名称）
    new_ssh_clicked = pyqtSignal()  # 点击新建SSH按钮
    new_serial_clicked = pyqtSignal()  # 点击新建串口按钮

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-right: 1px solid #3c3c3c;
            }
        """)
        self._init_ui()

    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题
        title = QLabel("会话")
        title.setStyleSheet("""
            QLabel {
                background-color: #3c3c3c;
                color: #cccccc;
                padding: 8px 10px;
                font-size: 13px;
                font-weight: bold;
                border-bottom: 1px solid #4c4c4c;
            }
        """)
        layout.addWidget(title)

        # 连接列表
        self.connections_list = QListWidget()
        self.connections_list.setFocusPolicy(Qt.NoFocus)
        self.connections_list.setContextMenuPolicy(Qt.CustomContextMenu)  # 启用自定义右键菜单
        self.connections_list.customContextMenuRequested.connect(self._show_context_menu)
        self.connections_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                border: none;
                outline: none;
                color: #cccccc;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px 10px;
                border-bottom: 1px solid #3c3c3c;
            }
            QListWidget::item:hover {
                background-color: #3c3c3c;
            }
            QListWidget::item:selected {
                background-color: #4c4c4c;
                color: #ffffff;
            }
        """)
        self.connections_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.connections_list)

        # 底部按钮
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(5)

        # SSH按钮
        self.btn_ssh = QPushButton("SSH")
        self.btn_ssh.setFocusPolicy(Qt.NoFocus)
        self.btn_ssh.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: #cccccc;
                border: none;
                padding: 6px;
                border-radius: 2px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #5c5c5c;
            }
        """)
        self.btn_ssh.clicked.connect(self.new_ssh_clicked.emit)
        button_layout.addWidget(self.btn_ssh)

        # 串口按钮
        self.btn_serial = QPushButton("串口")
        self.btn_serial.setFocusPolicy(Qt.NoFocus)
        self.btn_serial.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: #cccccc;
                border: none;
                padding: 6px;
                border-radius: 2px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #5c5c5c;
            }
        """)
        self.btn_serial.clicked.connect(self.new_serial_clicked.emit)
        button_layout.addWidget(self.btn_serial)

        layout.addLayout(button_layout)

    def load_connections(self, connections):
        """加载连接列表

        Args:
            connections: ConnectionConfig对象列表
        """
        self.connections_list.clear()

        if not connections:
            item = QListWidgetItem("无会话")
            item.setFlags(Qt.NoItemFlags)
            item.setForeground(Qt.gray)
            self.connections_list.addItem(item)
            return

        for conn in connections:
            item = QListWidgetItem(conn.display_name)
            item.setData(Qt.UserRole, conn)
            self.connections_list.addItem(item)

    def _on_item_double_clicked(self, item: QListWidgetItem):
        """列表项双击事件"""
        config = item.data(Qt.UserRole)
        if config:
            self.connection_selected.emit(config)

    def _show_context_menu(self, position):
        """显示右键菜单"""
        item = self.connections_list.itemAt(position)
        if not item:
            return

        config = item.data(Qt.UserRole)
        if not config:
            return

        # 创建右键菜单
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2b2b2b;
                color: #cccccc;
                border: 1px solid #3c3c3c;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3c3c3c;
            }
        """)

        # 连接动作
        connect_action = menu.addAction("连接")
        connect_action.triggered.connect(lambda: self.connection_selected.emit(config))

        menu.addSeparator()

        # 编辑动作
        edit_action = menu.addAction("编辑")
        edit_action.triggered.connect(lambda: self.connection_edit.emit(config))

        # 删除动作
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(lambda: self.connection_delete.emit(config.name))

        # 显示菜单
        menu.exec_(QCursor.pos())
