#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MShell - 跨平台终端工具
支持SSH和串口连接、自定义快捷键、颜色渲染、快捷指令和文件传输
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTabWidget,
                             QMessageBox, QInputDialog, QLineEdit)
from PyQt5.QtCore import Qt

# 导入已实现的模块
from mshell_platform import get_platform
from config.config_manager import ConfigManager
from terminal.terminal_widget import TerminalWidget
from core.ssh_connection import SSHConnection
from core.serial_connection import SerialConnection
from core.command_executor import CommandExecutor
from ui.connection_dialogs import (SSHConnectionDialog, SerialConnectionDialog,
                                   SavedConnectionsDialog)


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
