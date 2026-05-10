"""主窗口 - 使用分层架构重构"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QTabWidget, QMessageBox, QInputDialog, QLineEdit, QDialog, QAction)
from PyQt5.QtCore import Qt

from mshell_platform import get_platform
from services.config_service import ConfigService
from core.managers.connection_manager import ConnectionManager
from models.connection import SSHConnectionConfig, SerialConnectionConfig, create_connection_config
from terminal.terminal_widget import TerminalWidget
from ui.widgets.sidebar import Sidebar
from ui.widgets.welcome_page import WelcomePage
from ui.dialogs.connection_dialogs import SSHConnectionDialog, SerialConnectionDialog, SavedConnectionsDialog
from ui.dialogs.connection_close_dialog import ConnectionCloseDialog


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()

        # 初始化服务和管理器
        self.platform = get_platform()
        self.config_service = ConfigService()
        self.connection_manager = ConnectionManager()

        # 连接关闭行为配置
        self.auto_close_on_disconnect = None

        # 加载配置
        self.config_service.load()
        self.auto_close_on_disconnect = self.config_service.get_auto_close_on_disconnect()

        # 初始化UI
        self._init_ui()

        # 连接信号
        self._connect_signals()

    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("MShell - 跨平台终端工具")
        self.resize(1200, 800)
        self._center_window()

        # 创建菜单栏
        self._create_menu_bar()

        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧边栏
        self.sidebar = Sidebar()
        self.sidebar.load_connections(self.config_service.get_connections())
        main_layout.addWidget(self.sidebar)

        # 右侧主区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # 标签栏容器
        tab_bar_container = QWidget()
        tab_bar_container.setStyleSheet("QWidget { background-color: #3c3c3c; }")
        tab_bar_layout = QVBoxLayout(tab_bar_container)
        tab_bar_layout.setContentsMargins(0, 0, 0, 0)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setFocusPolicy(Qt.NoFocus)
        self.tab_widget.tabBar().setFocusPolicy(Qt.NoFocus)
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
        main_layout.addWidget(right_widget, 1)

        # 创建欢迎页
        welcome_page = WelcomePage(self.platform)
        self.tab_widget.addTab(welcome_page, "欢迎")

    def _create_menu_bar(self):
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

        from PyQt5.QtWidgets import QAction

        new_ssh_action = QAction("新建SSH连接(&S)", self)
        new_ssh_action.setShortcut("Ctrl+Shift+S")
        new_ssh_action.triggered.connect(self._on_new_ssh)
        file_menu.addAction(new_ssh_action)

        new_serial_action = QAction("新建串口连接(&P)", self)
        new_serial_action.setShortcut("Ctrl+Shift+P")
        new_serial_action.triggered.connect(self._on_new_serial)
        file_menu.addAction(new_serial_action)

        file_menu.addSeparator()

        saved_conn_action = QAction("已保存的连接(&C)...", self)
        saved_conn_action.setShortcut("Ctrl+O")
        saved_conn_action.triggered.connect(self._show_saved_connections)
        file_menu.addAction(saved_conn_action)

        file_menu.addSeparator()

        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 查看菜单
        view_menu = menubar.addMenu("查看(&V)")

        fullscreen_action = QAction("全屏(&F)", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

    def _connect_signals(self):
        """连接信号"""
        # 侧边栏信号
        self.sidebar.connection_selected.connect(self._on_connection_selected)
        self.sidebar.new_ssh_clicked.connect(self._on_new_ssh)
        self.sidebar.new_serial_clicked.connect(self._on_new_serial)

        # 连接管理器信号
        self.connection_manager.connection_created.connect(self._on_connection_created)
        self.connection_manager.connection_closed.connect(self._on_connection_closed)
        self.connection_manager.connection_error.connect(self._on_connection_error)

        # 标签页信号
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)

    def _center_window(self):
        """窗口居中"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def _toggle_fullscreen(self):
        """切换全屏"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _on_new_ssh(self):
        """新建SSH连接"""
        dialog = SSHConnectionDialog(self)
        if dialog.exec_():
            config_dict = dialog.get_config()
            config = create_connection_config(config_dict)

            # 保存配置
            if config_dict.get('name'):
                if not self.config_service.add_connection(config):
                    reply = QMessageBox.question(
                        self, '配置已存在',
                        f"连接 '{config.name}' 已存在，是否覆盖？",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.Yes:
                        self.config_service.update_connection(config)

                # 刷新侧边栏
                self.sidebar.load_connections(self.config_service.get_connections())

            # 建立连接
            self._create_connection(config)

    def _on_new_serial(self):
        """新建串口连接"""
        dialog = SerialConnectionDialog(self)
        if dialog.exec_():
            config_dict = dialog.get_config()
            config = create_connection_config(config_dict)

            # 保存配置
            if config_dict.get('name'):
                if not self.config_service.add_connection(config):
                    reply = QMessageBox.question(
                        self, '配置已存在',
                        f"连接 '{config.name}' 已存在，是否覆盖？",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.Yes:
                        self.config_service.update_connection(config)

                # 刷新侧边栏
                self.sidebar.load_connections(self.config_service.get_connections())

            # 建立连接
            self._create_connection(config)

    def _on_connection_selected(self, config):
        """侧边栏连接被选中"""
        # 如果是SSH连接且没有密码，询问密码
        if isinstance(config, SSHConnectionConfig):
            if not config.password and not config.key_file:
                password, ok = QInputDialog.getText(
                    self, "SSH连接",
                    f"请输入 {config.username}@{config.host} 的密码:",
                    QLineEdit.Password
                )
                if not ok:
                    return
                config._config['password'] = password

        self._create_connection(config)

    def _create_connection(self, config):
        """创建连接"""
        # 创建终端
        terminal = TerminalWidget()

        # 根据类型创建连接
        if isinstance(config, SSHConnectionConfig):
            session = self.connection_manager.create_ssh_connection(config, terminal)
        elif isinstance(config, SerialConnectionConfig):
            session = self.connection_manager.create_serial_connection(config, terminal)
        else:
            QMessageBox.warning(self, "错误", f"不支持的连接类型: {config.type}")
            return

        if not session:
            return

        # 添加到标签页
        index = self.tab_widget.addTab(terminal, config.name)
        self.tab_widget.setCurrentIndex(index)
        terminal.setFocus()

    def _on_connection_created(self, session):
        """连接创建成功"""
        pass  # 已在_create_connection中处理

    def _on_connection_closed(self, tab_index):
        """连接关闭"""
        # 根据配置决定是否关闭标签页
        if self.auto_close_on_disconnect is None:
            # 询问用户
            session = self.connection_manager.get_session(tab_index)
            if session:
                dialog = ConnectionCloseDialog(session.tab_name, self)
                result = dialog.exec_()

                if dialog.remember_choice:
                    self.auto_close_on_disconnect = (result == QDialog.Accepted)
                    self.config_service.set_auto_close_on_disconnect(self.auto_close_on_disconnect)

                if result == QDialog.Accepted:
                    self.tab_widget.removeTab(tab_index)
        elif self.auto_close_on_disconnect:
            self.tab_widget.removeTab(tab_index)

    def _on_connection_error(self, error_msg):
        """连接错误"""
        QMessageBox.warning(self, "连接错误", error_msg)

    def _on_tab_close_requested(self, index):
        """标签页关闭请求"""
        if index == 0:  # 欢迎页不能关闭
            return

        # 关闭连接
        self.connection_manager.close_connection(index)
        self.tab_widget.removeTab(index)

    def _show_saved_connections(self):
        """显示已保存的连接"""
        dialog = SavedConnectionsDialog(self, self.config_service._config_manager)
        if dialog.exec_() and dialog.selected_config:
            config = create_connection_config(dialog.selected_config)
            self._on_connection_selected(config)

    def closeEvent(self, event):
        """窗口关闭事件"""
        self.connection_manager.close_all_connections()
        event.accept()
