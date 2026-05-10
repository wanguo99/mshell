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
from platform import get_platform
from config.config_manager import ConfigManager
from terminal.terminal_widget import TerminalWidget
from core.ssh_connection import SSHConnection
from core.serial_connection import SerialConnection
from core.command_executor import CommandExecutor


class SimpleMainWindow(QMainWindow):
    """简单的主窗口 - 集成所有已完成的模块"""

    def __init__(self):
        super().__init__()
        self.platform = get_platform()
        self.config_manager = ConfigManager()  # 使用默认配置路径
        self.command_executor = CommandExecutor()
        self.connections = {}  # 存储连接对象

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("MShell - 跨平台终端工具")
        self.setGeometry(100, 100, 1200, 800)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 顶部工具栏
        toolbar_layout = QHBoxLayout()

        # 连接按钮
        self.btn_ssh = QPushButton("SSH连接")
        self.btn_ssh.clicked.connect(self.create_ssh_connection)
        toolbar_layout.addWidget(self.btn_ssh)

        self.btn_serial = QPushButton("串口连接")
        self.btn_serial.clicked.connect(self.create_serial_connection)
        toolbar_layout.addWidget(self.btn_serial)

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
            "点击上方按钮创建SSH或串口连接"
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

    def create_ssh_connection(self):
        """创建SSH连接"""
        # 简单的输入对话框
        host, ok = QInputDialog.getText(self, "SSH连接", "主机地址:", QLineEdit.Normal, "localhost")
        if not ok or not host:
            return

        username, ok = QInputDialog.getText(self, "SSH连接", "用户名:", QLineEdit.Normal, "root")
        if not ok or not username:
            return

        password, ok = QInputDialog.getText(self, "SSH连接", "密码:", QLineEdit.Password)
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
        if ssh.connect(host=host, username=username, password=password):
            tab_name = f"SSH - {host}"
            index = self.tab_widget.addTab(terminal, tab_name)
            self.tab_widget.setCurrentIndex(index)
            self.connections[index] = ssh
            self.status_label.setText(f"已连接到 {host}")
        else:
            QMessageBox.warning(self, "连接失败", f"无法连接到 {host}")
            self.status_label.setText("连接失败")

    def create_serial_connection(self):
        """创建串口连接"""
        # 获取可用串口
        ports = SerialConnection.list_available_ports()
        if not ports:
            QMessageBox.warning(self, "串口连接", "未找到可用的串口设备")
            return

        # 显示串口列表
        port_names = [p['device'] for p in ports]
        port, ok = QInputDialog.getItem(self, "串口连接", "选择串口:", port_names, 0, False)
        if not ok or not port:
            return

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
        if serial.connect(port=port, baudrate=115200):
            tab_name = f"Serial - {port}"
            index = self.tab_widget.addTab(terminal, tab_name)
            self.tab_widget.setCurrentIndex(index)
            self.connections[index] = serial
            self.status_label.setText(f"已连接到 {port}")
        else:
            QMessageBox.warning(self, "连接失败", f"无法打开串口 {port}")
            self.status_label.setText("连接失败")

    def close_tab(self, index):
        """关闭标签页"""
        if index == 0:  # 不关闭欢迎页
            return

        # 断开连接
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
        # 断开所有连接
        for conn in self.connections.values():
            conn.disconnect()
        event.accept()


def main():
    """应用程序入口"""
    app = QApplication(sys.argv)
    app.setApplicationName("MShell")
    app.setOrganizationName("MShell")

    # 创建主窗口
    window = SimpleMainWindow()
    window.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
