#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MShell - 跨平台终端工具
支持SSH和串口连接、自定义快捷键、颜色渲染、快捷指令和文件传输
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTabWidget,
                             QMessageBox, QInputDialog, QLineEdit, QDialog,
                             QFormLayout, QComboBox, QCheckBox, QListWidget,
                             QDialogButtonBox, QSpinBox)
from PyQt5.QtCore import Qt

# 导入已实现的模块
from mshell_platform import get_platform
from config.config_manager import ConfigManager
from terminal.terminal_widget import TerminalWidget
from core.ssh_connection import SSHConnection
from core.serial_connection import SerialConnection
from core.command_executor import CommandExecutor


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

        layout = QVBoxLayout(self)

        # 连接列表
        self.list_widget = QListWidget()
        self.load_connections()
        self.list_widget.itemDoubleClicked.connect(self.on_connect)
        layout.addWidget(self.list_widget)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.btn_connect = QPushButton("连接")
        self.btn_connect.clicked.connect(self.on_connect)
        button_layout.addWidget(self.btn_connect)

        self.btn_edit = QPushButton("编辑")
        self.btn_edit.clicked.connect(self.on_edit)
        button_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton("删除")
        self.btn_delete.clicked.connect(self.on_delete)
        button_layout.addWidget(self.btn_delete)

        button_layout.addStretch()

        self.btn_close = QPushButton("关闭")
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


class SimpleMainWindow(QMainWindow):
    """简单的主窗口 - 集成所有已完成的模块"""

    def __init__(self):
        super().__init__()
        self.platform = get_platform()
        self.config_manager = ConfigManager()
        self.command_executor = CommandExecutor()
        self.connections = {}

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("MShell - 跨平台终端工具")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # 顶部工具栏
        toolbar_layout = QHBoxLayout()

        # 新建连接按钮
        self.btn_ssh = QPushButton("新建SSH连接")
        self.btn_ssh.clicked.connect(self.create_ssh_connection)
        toolbar_layout.addWidget(self.btn_ssh)

        self.btn_serial = QPushButton("新建串口连接")
        self.btn_serial.clicked.connect(self.create_serial_connection)
        toolbar_layout.addWidget(self.btn_serial)

        # 已保存的连接按钮
        self.btn_saved = QPushButton("已保存的连接")
        self.btn_saved.clicked.connect(self.show_saved_connections)
        toolbar_layout.addWidget(self.btn_saved)

        toolbar_layout.addStretch()

        # 状态标签
        self.status_label = QLabel("就绪")
        toolbar_layout.addWidget(self.status_label)

        main_layout.addLayout(toolbar_layout)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        main_layout.addWidget(self.tab_widget)

        # 创建欢迎标签页
        self.create_welcome_tab()

    def create_welcome_tab(self):
        """创建欢迎标签页"""
        welcome_widget = QWidget()
        layout = QVBoxLayout(welcome_widget)

        title = QLabel("欢迎使用 MShell")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        info = QLabel(
            "MShell - 跨平台终端工具\n\n"
            "✓ 已集成模块:\n"
            "  • Platform 平台适配层\n"
            "  • Config 配置管理\n"
            "  • Terminal 终端渲染引擎\n"
            "  • Core 连接管理 (SSH/串口)\n"
            "  • File Transfer 文件传输\n\n"
            "点击上方按钮创建新连接或使用已保存的连接"
        )
        info.setStyleSheet("font-size: 14px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        # 显示平台信息
        platform_info = QLabel(
            f"\n平台信息:\n"
            f"  • 操作系统: {self.platform.__class__.__name__}\n"
            f"  • 默认字体: {self.platform.ui.get_default_font()[0]} {self.platform.ui.get_default_font()[1]}pt\n"
            f"  • 快捷键修饰符: {self.platform.ui.get_shortcut_modifier()}\n"
            f"  • 配置目录: {self.platform.config.get_config_dir()}\n"
        )
        platform_info.setStyleSheet("font-size: 12px; color: #666;")
        platform_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(platform_info)

        layout.addStretch()

        self.tab_widget.addTab(welcome_widget, "欢迎")

    def show_saved_connections(self):
        """显示已保存的连接"""
        dialog = SavedConnectionsDialog(self, self.config_manager)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_config:
            self.connect_with_config(dialog.selected_config)

    def create_ssh_connection(self):
        """创建SSH连接"""
        dialog = SSHConnectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()

            # 如果需要保存配置
            if config.get('name'):
                self.save_connection_config(config)

            # 建立连接
            self.connect_with_config(config)

    def create_serial_connection(self):
        """创建串口连接"""
        dialog = SerialConnectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()

            # 如果需要保存配置
            if config.get('name'):
                self.save_connection_config(config)

            # 建立连接
            self.connect_with_config(config)

    def save_connection_config(self, config):
        """保存连接配置"""
        connections = self.config_manager.get_connections()

        # 检查是否已存在同名配置
        existing = [c for c in connections if c.get('name') == config.get('name')]
        if existing:
            reply = QMessageBox.question(
                self, '配置已存在',
                f"连接 '{config.get('name')}' 已存在，是否覆盖？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                connections = [c for c in connections if c.get('name') != config.get('name')]
            else:
                return

        # 添加新配置（不保存密码）
        save_config = config.copy()
        if 'password' in save_config:
            del save_config['password']

        connections.append(save_config)
        self.config_manager.set('connections', connections)
        self.config_manager.save()

        QMessageBox.information(self, '保存成功', f"连接配置 '{config.get('name')}' 已保存")

    def connect_with_config(self, config):
        """使用配置建立连接"""
        if config.get('type') == 'ssh':
            self.connect_ssh(config)
        elif config.get('type') == 'serial':
            self.connect_serial(config)

    def connect_ssh(self, config):
        """建立SSH连接"""
        host = config.get('host')
        port = config.get('port', 22)
        username = config.get('username')
        password = config.get('password', '')
        key_file = config.get('key_file', '')

        # 如果没有密码且没有密钥，询问密码
        if not password and not key_file:
            password, ok = QInputDialog.getText(
                self, "SSH连接",
                f"请输入 {username}@{host} 的密码:",
                QLineEdit.Password
            )
            if not ok:
                return

        # 创建终端组件
        terminal = TerminalWidget()

        # 创建SSH连接
        ssh = SSHConnection()

        # 连接信号
        ssh.on_data_received = lambda data: terminal.write_output(data.decode('utf-8', errors='ignore'))
        ssh.on_connection_changed = lambda connected: self.update_connection_status(connected, f"SSH {host}")
        terminal.data_to_send.connect(ssh.send)

        # 尝试连接
        self.status_label.setText(f"正在连接 {host}...")

        connect_kwargs = {
            'host': host,
            'port': port,
            'username': username,
        }

        if key_file:
            connect_kwargs['key_file'] = key_file
        else:
            connect_kwargs['password'] = password

        if ssh.connect(**connect_kwargs):
            tab_name = config.get('name') or f"SSH - {host}"
            index = self.tab_widget.addTab(terminal, tab_name)
            self.tab_widget.setCurrentIndex(index)
            self.connections[index] = ssh
            self.status_label.setText(f"已连接到 {host}")
        else:
            QMessageBox.warning(self, "连接失败", f"无法连接到 {host}")
            self.status_label.setText("连接失败")

    def connect_serial(self, config):
        """建立串口连接"""
        port = config.get('port')
        baudrate = config.get('baudrate', 115200)
        bytesize = config.get('bytesize', 8)
        parity = config.get('parity', 'N')
        stopbits = config.get('stopbits', 1)

        # 创建终端组件
        terminal = TerminalWidget()

        # 创建串口连接
        serial = SerialConnection()

        # 连接信号
        serial.on_data_received = lambda data: terminal.write_output(data.decode('utf-8', errors='ignore'))
        serial.on_connection_changed = lambda connected: self.update_connection_status(connected, f"Serial {port}")
        terminal.data_to_send.connect(serial.send)

        # 尝试连接
        self.status_label.setText(f"正在连接 {port}...")
        if serial.connect(port=port, baudrate=baudrate, bytesize=bytesize,
                         parity=parity, stopbits=stopbits):
            tab_name = config.get('name') or f"Serial - {port}"
            index = self.tab_widget.addTab(terminal, tab_name)
            self.tab_widget.setCurrentIndex(index)
            self.connections[index] = serial
            self.status_label.setText(f"已连接到 {port}")
        else:
            QMessageBox.warning(self, "连接失败", f"无法打开串口 {port}")
            self.status_label.setText("连接失败")

    def close_tab(self, index):
        """关闭标签页"""
        if index == 0:
            return

        if index in self.connections:
            self.connections[index].disconnect()
            del self.connections[index]

        self.tab_widget.removeTab(index)

    def update_connection_status(self, connected, name):
        """更新连接状态"""
        status = "已连接" if connected else "已断开"
        self.status_label.setText(f"{name}: {status}")

    def load_config(self):
        """加载配置"""
        try:
            self.config_manager.load()
            print("配置加载成功")
        except Exception as e:
            print(f"配置加载失败: {e}")

    def closeEvent(self, event):
        """关闭事件"""
        for conn in self.connections.values():
            conn.disconnect()
        event.accept()


def main():
    """应用程序入口"""
    app = QApplication(sys.argv)
    app.setApplicationName("MShell")
    app.setOrganizationName("MShell")

    window = SimpleMainWindow()
    window.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
