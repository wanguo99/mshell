"""连接配置对话框

包含SSH和串口连接的配置对话框，以及已保存连接的管理对话框。
"""

from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QSpinBox,
                             QComboBox, QCheckBox, QDialogButtonBox,
                             QListWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

from core.serial_connection import SerialConnection
from ui.theme import Theme, get_stylesheet


class SSHConnectionDialog(QDialog):
    """SSH连接配置对话框"""

    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config or {}
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("SSH连接配置")
        self.setMinimumWidth(400)
        self.setStyleSheet(get_stylesheet("dialog"))

        layout = QFormLayout(self)

        # 连接名称
        self.name_edit = QLineEdit(self.config.get('name', ''))
        layout.addRow("连接名称:", self.name_edit)

        # 主机地址
        self.host_edit = QLineEdit(self.config.get('host', 'localhost'))
        layout.addRow("主机地址:", self.host_edit)

        # 端口
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(self.config.get('port', 22))
        layout.addRow("端口:", self.port_spin)

        # 用户名
        self.username_edit = QLineEdit(self.config.get('username', 'root'))
        layout.addRow("用户名:", self.username_edit)

        # 认证方式
        self.auth_combo = QComboBox()
        self.auth_combo.addItems(['密码', '密钥'])
        auth_type = self.config.get('auth_type', 'password')
        self.auth_combo.setCurrentIndex(0 if auth_type == 'password' else 1)
        layout.addRow("认证方式:", self.auth_combo)

        # 密码
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("密码:", self.password_edit)

        # 密钥文件
        self.keyfile_edit = QLineEdit(self.config.get('key_file', ''))
        layout.addRow("密钥文件:", self.keyfile_edit)

        # 保存配置选项
        self.save_check = QCheckBox("保存此连接配置")
        self.save_check.setChecked(bool(self.config.get('name')))
        layout.addRow("", self.save_check)

        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.button(QDialogButtonBox.Ok).setStyleSheet(get_stylesheet("button_primary"))
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(get_stylesheet("button"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_config(self):
        """获取配置"""
        config = {
            'type': 'ssh',
            'host': self.host_edit.text(),
            'port': self.port_spin.value(),
            'username': self.username_edit.text(),
            'auth_type': 'password' if self.auth_combo.currentIndex() == 0 else 'key',
            'password': self.password_edit.text(),
            'key_file': self.keyfile_edit.text(),
        }

        if self.save_check.isChecked():
            config['name'] = self.name_edit.text() or f"SSH-{config['host']}"

        return config


class SerialConnectionDialog(QDialog):
    """串口连接配置对话框"""

    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config or {}
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("串口连接配置")
        self.setMinimumWidth(400)
        self.setStyleSheet(get_stylesheet("dialog"))

        layout = QFormLayout(self)

        # 连接名称
        self.name_edit = QLineEdit(self.config.get('name', ''))
        layout.addRow("连接名称:", self.name_edit)

        # 串口选择
        self.port_combo = QComboBox()
        ports = SerialConnection.list_available_ports()
        for port in ports:
            self.port_combo.addItem(f"{port['device']} - {port['description']}", port['device'])

        # 设置当前值
        if self.config.get('port'):
            index = self.port_combo.findData(self.config['port'])
            if index >= 0:
                self.port_combo.setCurrentIndex(index)

        layout.addRow("串口:", self.port_combo)

        # 波特率
        self.baudrate_combo = QComboBox()
        baudrates = ['9600', '19200', '38400', '57600', '115200', '230400', '460800', '921600']
        self.baudrate_combo.addItems(baudrates)
        baudrate = str(self.config.get('baudrate', 115200))
        index = self.baudrate_combo.findText(baudrate)
        if index >= 0:
            self.baudrate_combo.setCurrentIndex(index)
        layout.addRow("波特率:", self.baudrate_combo)

        # 数据位
        self.bytesize_combo = QComboBox()
        self.bytesize_combo.addItems(['5', '6', '7', '8'])
        self.bytesize_combo.setCurrentText(str(self.config.get('bytesize', 8)))
        layout.addRow("数据位:", self.bytesize_combo)

        # 校验位
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(['无(N)', '偶(E)', '奇(O)', '标记(M)', '空格(S)'])
        parity_map = {'N': 0, 'E': 1, 'O': 2, 'M': 3, 'S': 4}
        self.parity_combo.setCurrentIndex(parity_map.get(self.config.get('parity', 'N'), 0))
        layout.addRow("校验位:", self.parity_combo)

        # 停止位
        self.stopbits_combo = QComboBox()
        self.stopbits_combo.addItems(['1', '1.5', '2'])
        self.stopbits_combo.setCurrentText(str(self.config.get('stopbits', 1)))
        layout.addRow("停止位:", self.stopbits_combo)

        # 保存配置选项
        self.save_check = QCheckBox("保存此连接配置")
        self.save_check.setChecked(bool(self.config.get('name')))
        layout.addRow("", self.save_check)

        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.button(QDialogButtonBox.Ok).setStyleSheet(get_stylesheet("button_primary"))
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(get_stylesheet("button"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_config(self):
        """获取配置"""
        parity_map = ['N', 'E', 'O', 'M', 'S']

        config = {
            'type': 'serial',
            'port': self.port_combo.currentData(),
            'baudrate': int(self.baudrate_combo.currentText()),
            'bytesize': int(self.bytesize_combo.currentText()),
            'parity': parity_map[self.parity_combo.currentIndex()],
            'stopbits': float(self.stopbits_combo.currentText()),
        }

        if self.save_check.isChecked():
            config['name'] = self.name_edit.text() or f"Serial-{config['port']}"

        return config


class SavedConnectionsDialog(QDialog):
    """已保存的连接对话框"""

    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.selected_config = None
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("已保存的连接")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(get_stylesheet("dialog"))

        layout = QVBoxLayout(self)

        # 连接列表
        self.list_widget = QListWidget()
        self.load_connections()
        self.list_widget.itemDoubleClicked.connect(self.on_connect)
        layout.addWidget(self.list_widget)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.btn_connect = QPushButton("连接")
        self.btn_connect.setStyleSheet(get_stylesheet("button_primary"))
        self.btn_connect.clicked.connect(self.on_connect)
        button_layout.addWidget(self.btn_connect)

        self.btn_edit = QPushButton("编辑")
        self.btn_edit.setStyleSheet(get_stylesheet("button"))
        self.btn_edit.clicked.connect(self.on_edit)
        button_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton("删除")
        self.btn_delete.setStyleSheet(get_stylesheet("button"))
        self.btn_delete.clicked.connect(self.on_delete)
        button_layout.addWidget(self.btn_delete)

        button_layout.addStretch()

        self.btn_close = QPushButton("关闭")
        self.btn_close.setStyleSheet(get_stylesheet("button"))
        self.btn_close.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_close)

        layout.addLayout(button_layout)

    def load_connections(self):
        """加载连接列表"""
        self.list_widget.clear()
        connections = self.config_manager.get_connections()

        for conn in connections:
            if conn.get('type') == 'ssh':
                text = f"[SSH] {conn.get('name', 'Unnamed')} - {conn.get('host')}:{conn.get('port', 22)}"
            elif conn.get('type') == 'serial':
                text = f"[Serial] {conn.get('name', 'Unnamed')} - {conn.get('port')} @ {conn.get('baudrate', 115200)}"
            else:
                text = f"[Unknown] {conn.get('name', 'Unnamed')}"

            item = self.list_widget.addItem(text)
            self.list_widget.item(self.list_widget.count() - 1).setData(Qt.UserRole, conn)

    def on_connect(self):
        """连接选中的配置"""
        current_item = self.list_widget.currentItem()
        if current_item:
            self.selected_config = current_item.data(Qt.UserRole)
            self.accept()

    def on_edit(self):
        """编辑选中的配置"""
        current_item = self.list_widget.currentItem()
        if not current_item:
            return

        config = current_item.data(Qt.UserRole)

        if config.get('type') == 'ssh':
            dialog = SSHConnectionDialog(self, config)
        elif config.get('type') == 'serial':
            dialog = SerialConnectionDialog(self, config)
        else:
            return

        if dialog.exec_() == QDialog.Accepted:
            new_config = dialog.get_config()
            # 更新配置
            connections = self.config_manager.get_connections()
            for i, conn in enumerate(connections):
                if conn.get('name') == config.get('name'):
                    connections[i] = new_config
                    break
            self.config_manager.set('connections', connections)
            self.config_manager.save()
            self.load_connections()

    def on_delete(self):
        """删除选中的配置"""
        current_item = self.list_widget.currentItem()
        if not current_item:
            return

        config = current_item.data(Qt.UserRole)
        reply = QMessageBox.question(
            self, '确认删除',
            f"确定要删除连接 '{config.get('name')}' 吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            connections = self.config_manager.get_connections()
            connections = [c for c in connections if c.get('name') != config.get('name')]
            self.config_manager.set('connections', connections)
            self.config_manager.save()
            self.load_connections()
