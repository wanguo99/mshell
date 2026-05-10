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
                             QMenuBar, QMenu, QAction, QListWidget, QListWidgetItem,
                             QSplitter)
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
from ui.connection_close_dialog import ConnectionCloseDialog


class SimpleMainWindow(QMainWindow):
    """简单的主窗口 - 集成所有已完成的模块"""

    def __init__(self):
        super().__init__()
        self.platform = get_platform()
        self.config_manager = ConfigManager()
        self.command_executor = CommandExecutor()
        self.connections = {}
        self.tab_names = {}  # 存储标签页名称

        # 连接关闭行为配置
        self.auto_close_on_disconnect = None  # None=询问, True=自动关闭, False=不关闭

        self.load_config()
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("MShell - 跨平台终端工具")

        # 设置窗口大小
        window_width = 1200
        window_height = 800
        self.resize(window_width, window_height)

        # 居中显示窗口
        self.center_window()

        # 创建菜单栏
        self.create_menu_bar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧边栏：已保存的连接
        self.create_sidebar()

        # 右侧主区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # 标签栏区域
        tab_bar_container = QWidget()
        tab_bar_container.setStyleSheet("""
            QWidget {
                background-color: #3c3c3c;
            }
        """)
        tab_bar_layout = QVBoxLayout(tab_bar_container)
        tab_bar_layout.setContentsMargins(0, 0, 0, 0)
        tab_bar_layout.setSpacing(0)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setFocusPolicy(Qt.NoFocus)  # 标签页本身不接受焦点

        # 禁用标签栏的焦点，确保Tab键不会切换标签
        tab_bar = self.tab_widget.tabBar()
        tab_bar.setFocusPolicy(Qt.NoFocus)

        # 设置标签栏样式，使用深色主题
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3c3c3c;
                background-color: #000000;
                top: -1px;
            }
            QTabBar {
                background-color: #3c3c3c;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: #aaaaaa;
                border: 1px solid #4c4c4c;
                border-bottom: none;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #000000;
                color: #cccccc;
                border-bottom: 1px solid #000000;
            }
            QTabBar::tab:hover {
                background-color: #4c4c4c;
                color: #cccccc;
            }
        """)

        tab_bar_layout.addWidget(self.tab_widget)
        right_layout.addWidget(tab_bar_container)

        # 创建欢迎标签页
        self.create_welcome_tab()

        # 添加到主布局
        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(right_widget, 1)  # 右侧占据剩余空间

    def create_sidebar(self):
        """创建左侧边栏"""
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setFixedWidth(200)
        self.sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-right: 1px solid #3c3c3c;
            }
        """)

        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # 侧边栏标题
        sidebar_title = QLabel("会话")
        sidebar_title.setStyleSheet("""
            QLabel {
                background-color: #3c3c3c;
                color: #cccccc;
                padding: 8px 10px;
                font-size: 13px;
                font-weight: bold;
                border-bottom: 1px solid #4c4c4c;
            }
        """)
        sidebar_layout.addWidget(sidebar_title)

        # 连接列表
        self.sidebar_connections_list = QListWidget()
        self.sidebar_connections_list.setFocusPolicy(Qt.NoFocus)  # 不接受焦点
        self.sidebar_connections_list.setStyleSheet("""
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
        self.sidebar_connections_list.itemDoubleClicked.connect(self.on_sidebar_connection_double_clicked)
        sidebar_layout.addWidget(self.sidebar_connections_list)

        # 底部按钮区域
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(5)

        # 新建SSH按钮
        btn_new_ssh = QPushButton("SSH")
        btn_new_ssh.setFocusPolicy(Qt.NoFocus)  # 完全不接受焦点
        btn_new_ssh.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: #cccccc;
                border: 1px solid #4c4c4c;
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
        btn_new_ssh.clicked.connect(self.create_ssh_connection)
        button_layout.addWidget(btn_new_ssh)

        # 新建串口按钮
        btn_new_serial = QPushButton("串口")
        btn_new_serial.setFocusPolicy(Qt.NoFocus)  # 完全不接受焦点
        btn_new_serial.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: #cccccc;
                border: 1px solid #4c4c4c;
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
        btn_new_serial.clicked.connect(self.create_serial_connection)
        button_layout.addWidget(btn_new_serial)

        sidebar_layout.addLayout(button_layout)

        # 加载连接列表
        self.load_sidebar_connections()

    def load_sidebar_connections(self):
        """加载侧边栏连接列表"""
        self.sidebar_connections_list.clear()
        connections = self.config_manager.get_connections()

        if not connections:
            item = QListWidgetItem("无会话")
            item.setFlags(Qt.NoItemFlags)
            item.setForeground(Qt.gray)
            self.sidebar_connections_list.addItem(item)
            return

        for conn in connections:
            conn_type = conn.get('type', 'unknown')
            conn_name = conn.get('name', 'Unnamed')

            if conn_type == 'ssh':
                host = conn.get('host', '')
                username = conn.get('username', '')
                display_text = f"{conn_name}\n{username}@{host}"
            elif conn_type == 'serial':
                port = conn.get('port', '')
                display_text = f"{conn_name}\n{port}"
            else:
                display_text = f"{conn_name}"

            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, conn)
            self.sidebar_connections_list.addItem(item)

    def on_sidebar_connection_double_clicked(self, item):
        """侧边栏连接双击事件"""
        conn_config = item.data(Qt.UserRole)
        if conn_config:
            self.connect_with_config(conn_config)

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2b2b2b;
                color: #cccccc;
                border-bottom: 1px solid #3c3c3c;
                padding: 2px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 10px;
            }
            QMenuBar::item:selected {
                background-color: #3c3c3c;
            }
            QMenuBar::item:pressed {
                background-color: #4c4c4c;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #cccccc;
                border: 1px solid #3c3c3c;
            }
            QMenu::item {
                padding: 5px 25px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3c3c3c;
            }
            QMenu::separator {
                height: 1px;
                background-color: #3c3c3c;
                margin: 2px 0px;
            }
        """)

        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")

        new_ssh_action = QAction("新建SSH连接(&S)", self)
        new_ssh_action.setShortcut("Ctrl+Shift+S")
        new_ssh_action.triggered.connect(self.create_ssh_connection)
        file_menu.addAction(new_ssh_action)

        new_serial_action = QAction("新建串口连接(&P)", self)
        new_serial_action.setShortcut("Ctrl+Shift+P")
        new_serial_action.triggered.connect(self.create_serial_connection)
        file_menu.addAction(new_serial_action)

        file_menu.addSeparator()

        saved_conn_action = QAction("已保存的连接(&C)...", self)
        saved_conn_action.setShortcut("Ctrl+O")
        saved_conn_action.triggered.connect(self.show_saved_connections)
        file_menu.addAction(saved_conn_action)

        file_menu.addSeparator()

        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑(&E)")

        copy_action = QAction("复制(&C)", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.setEnabled(False)  # 暂时禁用，后续实现
        edit_menu.addAction(copy_action)

        paste_action = QAction("粘贴(&V)", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.setEnabled(False)  # 暂时禁用，后续实现
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        select_all_action = QAction("全选(&A)", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.setEnabled(False)  # 暂时禁用，后续实现
        edit_menu.addAction(select_all_action)

        edit_menu.addSeparator()

        clear_action = QAction("清屏(&L)", self)
        clear_action.setShortcut("Ctrl+L")
        clear_action.setEnabled(False)  # 暂时禁用，后续实现
        edit_menu.addAction(clear_action)

        # 查看菜单
        view_menu = menubar.addMenu("查看(&V)")

        fullscreen_action = QAction("全屏(&F)", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        view_menu.addSeparator()

        zoom_in_action = QAction("放大(&I)", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.setEnabled(False)  # 暂时禁用，后续实现
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("缩小(&O)", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.setEnabled(False)  # 暂时禁用，后续实现
        view_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("重置缩放(&R)", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.setEnabled(False)  # 暂时禁用，后续实现
        view_menu.addAction(reset_zoom_action)

    def toggle_fullscreen(self):
        """切换全屏模式"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def create_welcome_tab(self):
        """创建欢迎标签页"""
        welcome_widget = QWidget()
        welcome_widget.setStyleSheet("""
            QWidget {
                background-color: #000000;
            }
        """)
        layout = QVBoxLayout(welcome_widget)
        layout.addStretch(2)

        title = QLabel("MShell")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #cccccc; background-color: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("跨平台终端工具")
        subtitle.setStyleSheet("font-size: 16px; color: #aaaaaa; background-color: transparent; margin-top: 10px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        info = QLabel(
            "从左侧边栏选择已保存的会话\n"
            "或点击底部按钮创建新连接"
        )
        info.setStyleSheet("font-size: 14px; color: #888888; background-color: transparent; line-height: 1.6;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        layout.addStretch(3)

        self.tab_widget.addTab(welcome_widget, "欢迎")

    def center_window(self):
        """将窗口居中显示在屏幕上"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

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

        # 刷新侧边栏连接列表
        self.load_sidebar_connections()

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

        # 连接数据信号（线程安全）
        ssh.data_received.connect(lambda data: terminal.write_output(data.decode('utf-8', errors='ignore')))
        terminal.data_to_send.connect(ssh.send)

        # 尝试连接
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
            # 通知SSH终端大小
            ssh.resize_terminal(terminal.cols, terminal.rows)

            tab_name = config.get('name') or f"SSH - {host}"
            index = self.tab_widget.addTab(terminal, tab_name)
            self.tab_widget.setCurrentIndex(index)
            self.connections[index] = ssh
            self.tab_names[index] = tab_name

            # 确保焦点在终端上
            terminal.setFocus()

            # 连接状态变化信号（需要索引信息）
            ssh.connection_changed.connect(lambda connected: self.handle_connection_changed(index, connected, tab_name))
        else:
            QMessageBox.warning(self, "连接失败", f"无法连接到 {host}")

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

        # 连接数据信号（线程安全）
        serial.data_received.connect(lambda data: terminal.write_output(data.decode('utf-8', errors='ignore')))
        terminal.data_to_send.connect(serial.send)

        # 尝试连接
        if serial.connect(port=port, baudrate=baudrate, bytesize=bytesize,
                         parity=parity, stopbits=stopbits):
            tab_name = config.get('name') or f"Serial - {port}"
            index = self.tab_widget.addTab(terminal, tab_name)
            self.tab_widget.setCurrentIndex(index)
            self.connections[index] = serial
            self.tab_names[index] = tab_name

            # 确保焦点在终端上
            terminal.setFocus()

            # 连接状态变化信号（需要索引信息）
            serial.connection_changed.connect(lambda connected: self.handle_connection_changed(index, connected, tab_name))
        else:
            QMessageBox.warning(self, "连接失败", f"无法打开串口 {port}")

    def close_tab(self, index):
        """关闭标签页"""
        if index == 0:
            return

        # 先断开连接（如果存在）
        if index in self.connections:
            conn = self.connections[index]
            # 断开信号连接，避免递归
            try:
                conn.connection_changed.disconnect()
            except:
                pass
            # 断开连接
            conn.disconnect()
            del self.connections[index]

        if index in self.tab_names:
            del self.tab_names[index]

        self.tab_widget.removeTab(index)

    def handle_connection_changed(self, tab_index, connected, connection_name):
        """处理连接状态变化

        Args:
            tab_index: 标签页索引
            connected: 是否已连接
            connection_name: 连接名称
        """
        if not connected:
            # 连接断开

            # 检查是否需要关闭标签页
            if self.auto_close_on_disconnect is None:
                # 询问用户
                dialog = ConnectionCloseDialog(connection_name, self)
                result = dialog.exec_()

                if dialog.remember_choice:
                    # 记住用户选择
                    self.auto_close_on_disconnect = (result == QDialog.Accepted)
                    # 保存到配置
                    self.config_manager.set('auto_close_on_disconnect', self.auto_close_on_disconnect)
                    self.config_manager.save()

                if result == QDialog.Accepted:
                    # 用户选择关闭
                    self.close_tab(tab_index)
            elif self.auto_close_on_disconnect:
                # 自动关闭
                self.close_tab(tab_index)
            # else: 不关闭，保持标签页


    def load_config(self):
        """加载配置"""
        try:
            self.config_manager.load()

            # 加载连接关闭行为配置
            auto_close = self.config_manager.get('auto_close_on_disconnect')
            if auto_close is not None:
                self.auto_close_on_disconnect = auto_close

            print("配置加载成功")
        except Exception as e:
            print(f"配置加载失败: {e}")

    def closeEvent(self, event):
        """关闭事件"""
        # 复制连接列表，避免在迭代时修改字典
        connections = list(self.connections.values())
        for conn in connections:
            try:
                # 断开信号连接，避免触发关闭对话框
                conn.connection_changed.disconnect()
            except:
                pass
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
