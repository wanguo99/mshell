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
from ui.dialogs.settings_dialog import SettingsDialog
from ui.theme import Theme, get_stylesheet, set_theme


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()

        # 初始化服务和管理器
        self.platform = get_platform()
        self.config_service = ConfigService()
        self.connection_manager = ConnectionManager()

        # 会话映射：terminal widget -> session
        self.terminal_to_session = {}

        # 连接关闭行为配置
        self.auto_close_on_disconnect = None
        self.confirm_exit_with_connections = None

        # 加载配置
        self.config_service.load()
        self.auto_close_on_disconnect = self.config_service.get_auto_close_on_disconnect()
        self.confirm_exit_with_connections = self.config_service.get('confirm_exit_with_connections')

        # 设置主题
        theme_name = self.config_service.get('application', {}).get('theme', 'dark')
        set_theme(theme_name)

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
        tab_bar_container.setStyleSheet(f"QWidget {{ background-color: {Theme.TAB_BG}; }}")
        tab_bar_layout = QVBoxLayout(tab_bar_container)
        tab_bar_layout.setContentsMargins(0, 0, 0, 0)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setFocusPolicy(Qt.NoFocus)
        self.tab_widget.tabBar().setFocusPolicy(Qt.NoFocus)
        self.tab_widget.setStyleSheet(get_stylesheet("tabwidget"))

        tab_bar_layout.addWidget(self.tab_widget)
        right_layout.addWidget(tab_bar_container)
        main_layout.addWidget(right_widget, 1)

        # 创建欢迎页
        welcome_page = WelcomePage(self.platform)
        self.tab_widget.addTab(welcome_page, "欢迎")

    def _create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        menubar.setStyleSheet(get_stylesheet("menubar"))

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

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑(&E)")

        scrollback_action = QAction("设置缓冲区大小(&B)...", self)
        scrollback_action.triggered.connect(self._set_scrollback_size)
        edit_menu.addAction(scrollback_action)

        # 工具菜单
        tools_menu = menubar.addMenu("工具(&T)")

        settings_action = QAction("设置(&S)...", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._show_settings)
        tools_menu.addAction(settings_action)

    def _connect_signals(self):
        """连接信号"""
        # 侧边栏信号
        self.sidebar.connection_selected.connect(self._on_connection_selected)
        self.sidebar.connection_edit.connect(self._on_connection_edit)
        self.sidebar.connection_delete.connect(self._on_connection_delete)
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

    def _set_scrollback_size(self):
        """设置终端缓冲区大小"""
        terminal_config = self.config_service.get('terminal', {})
        current_size = terminal_config.get('scrollback_lines', 10000)

        size, ok = QInputDialog.getInt(
            self,
            '设置缓冲区大小',
            '请输入缓冲区行数（100-100000）：',
            current_size,
            100,
            100000,
            1000
        )

        if ok:
            # 更新配置
            self.config_service.set('terminal.scrollback_lines', size)
            self.config_service.save()

            # 更新所有打开的终端
            for session in self.connection_manager.get_all_sessions():
                if session.terminal:
                    session.terminal.set_scrollback_lines(size)

            QMessageBox.information(
                self,
                '设置成功',
                f'缓冲区大小已设置为 {size} 行\n新设置将应用于所有打开的终端'
            )

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

    def _on_connection_edit(self, config):
        """编辑连接配置"""
        # 根据连接类型打开相应的编辑对话框
        # 将ConnectionConfig对象转换为字典
        config_dict = config.config_dict

        if isinstance(config, SSHConnectionConfig):
            dialog = SSHConnectionDialog(self, config_dict)
        else:
            dialog = SerialConnectionDialog(self, config_dict)

        if dialog.exec_():
            new_config_dict = dialog.get_config()
            # 保持原有的ID
            new_config_dict['id'] = config.id
            new_config = create_connection_config(new_config_dict)

            # 通过ID更新配置
            if self.config_service.update_connection(new_config):
                self.sidebar.load_connections(self.config_service.get_connections())
                QMessageBox.information(self, '编辑成功', f"连接 '{new_config.name}' 已更新")
            else:
                QMessageBox.warning(self, '编辑失败', f"无法更新连接 '{new_config.name}'")

    def _on_connection_delete(self, connection_id):
        """删除连接配置"""
        # 通过ID查找连接名称用于显示
        connections = self.config_service.get_connections()
        connection_name = None
        for conn in connections:
            if conn.id == connection_id:
                connection_name = conn.name
                break

        if not connection_name:
            QMessageBox.warning(self, '删除失败', '找不到指定的连接')
            return

        reply = QMessageBox.question(
            self, '确认删除',
            f"确定要删除连接 '{connection_name}' 吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.config_service.delete_connection(connection_id):
                # 刷新侧边栏
                self.sidebar.load_connections(self.config_service.get_connections())
                QMessageBox.information(self, '删除成功', f"连接 '{connection_name}' 已删除")
            else:
                QMessageBox.warning(self, '删除失败', f"无法删除连接 '{connection_name}'")

    def _create_connection(self, config):
        """创建连接"""
        # 获取终端配置
        terminal_config = self.config_service.get('terminal', {})
        scrollback_lines = terminal_config.get('scrollback_lines', 10000)

        # 创建终端
        terminal = TerminalWidget(scrollback_lines=scrollback_lines)

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

        # 检查是否需要替换欢迎页
        replace_welcome = self.config_service.get('application', {}).get('replace_welcome_page', False)

        if replace_welcome and self.tab_widget.count() > 0:
            # 检查第一个标签页是否是欢迎页
            first_widget = self.tab_widget.widget(0)
            if isinstance(first_widget, WelcomePage):
                # 替换欢迎页
                self.tab_widget.removeTab(0)
                index = self.tab_widget.insertTab(0, terminal, config.name)
                self.tab_widget.setCurrentIndex(0)
            else:
                # 正常添加标签页
                index = self.tab_widget.addTab(terminal, config.name)
                self.tab_widget.setCurrentIndex(index)
        else:
            # 正常添加标签页
            index = self.tab_widget.addTab(terminal, config.name)
            self.tab_widget.setCurrentIndex(index)

        terminal.setFocus()

        # 设置会话的标签页索引
        session.tab_index = index

        # 保存终端到会话的映射
        self.terminal_to_session[terminal] = session

    def _on_connection_created(self, session):
        """连接创建成功"""
        pass  # 已在_create_connection中处理

    def _on_connection_closed(self, session_id):
        """连接关闭"""
        # 根据session_id找到对应的session
        session = self.connection_manager.get_session(session_id)
        if not session:
            return

        terminal = session.terminal

        # 找到terminal在tab_widget中的实际索引
        actual_tab_index = -1
        for i in range(self.tab_widget.count()):
            if self.tab_widget.widget(i) == terminal:
                actual_tab_index = i
                break

        if actual_tab_index == -1:
            return

        # 根据配置决定是否关闭标签页
        if self.auto_close_on_disconnect is None:
            # 询问用户
            dialog = ConnectionCloseDialog(session.tab_name, self)
            result = dialog.exec_()

            if dialog.remember_choice:
                self.auto_close_on_disconnect = (result == QDialog.Accepted)
                self.config_service.set_auto_close_on_disconnect(self.auto_close_on_disconnect)

            if result == QDialog.Accepted:
                # 先从映射中移除
                if terminal in self.terminal_to_session:
                    del self.terminal_to_session[terminal]
                # 从连接管理器中移除
                self.connection_manager.close_connection(session_id)
                # 移除标签页
                self.tab_widget.removeTab(actual_tab_index)
        elif self.auto_close_on_disconnect:
            # 先从映射中移除
            if terminal in self.terminal_to_session:
                del self.terminal_to_session[terminal]
            # 从连接管理器中移除
            self.connection_manager.close_connection(session_id)
            # 移除标签页
            self.tab_widget.removeTab(actual_tab_index)

    def _on_connection_error(self, error_msg):
        """连接错误"""
        QMessageBox.warning(self, "连接错误", error_msg)

    def _on_tab_close_requested(self, index):
        """标签页关闭请求"""
        if index == 0:  # 欢迎页不能关闭
            return

        # 获取要关闭的terminal widget
        terminal = self.tab_widget.widget(index)

        # 查找对应的session
        session = self.terminal_to_session.get(terminal)
        if session:
            # 关闭连接
            self.connection_manager.close_connection(session.session_id)
            # 清除映射
            del self.terminal_to_session[terminal]

        # 移除标签页
        self.tab_widget.removeTab(index)

    def _show_saved_connections(self):
        """显示已保存的连接"""
        dialog = SavedConnectionsDialog(self, self.config_service._config_manager)
        if dialog.exec_() and dialog.selected_config:
            config = create_connection_config(dialog.selected_config)
            self._on_connection_selected(config)

    def _show_settings(self):
        """显示设置对话框"""
        # 保存当前主题
        old_theme = self.config_service.get('application', {}).get('theme', 'dark')

        dialog = SettingsDialog(self.config_service, self)
        if dialog.exec_():
            # 获取新主题
            new_theme = self.config_service.get('application', {}).get('theme', 'dark')

            # 应用侧边栏显示设置
            show_sidebar = self.config_service.get('ui', {}).get('show_sidebar', True)
            self.sidebar.setVisible(show_sidebar)

            # 重新加载配置到内存
            self.auto_close_on_disconnect = self.config_service.get_auto_close_on_disconnect()
            self.confirm_exit_with_connections = self.config_service.get('confirm_exit_with_connections')

            # 检查主题是否改变
            if old_theme != new_theme:
                QMessageBox.information(
                    self,
                    '设置已保存',
                    '设置已成功保存。主题、字体等设置需要重启应用后生效。'
                )
            else:
                QMessageBox.information(
                    self,
                    '设置已保存',
                    '设置已成功保存。'
                )

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 检查是否有活动连接（排除欢迎页）
        active_sessions = self.connection_manager.get_all_sessions()
        open_tabs_count = self.tab_widget.count() - 1  # 减去欢迎页

        if open_tabs_count > 0 and self.confirm_exit_with_connections is None:
            # 有打开的标签页且未设置自动确认，询问用户
            from PyQt5.QtWidgets import QMessageBox, QCheckBox

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("确认退出")
            msg_box.setIcon(QMessageBox.Question)

            # 显示活动连接数和总标签页数
            if active_sessions:
                msg_box.setText(f"当前有 {len(active_sessions)} 个活动连接，{open_tabs_count} 个打开的标签页")
            else:
                msg_box.setText(f"当前有 {open_tabs_count} 个打开的标签页")

            msg_box.setInformativeText("确定要关闭所有标签页并退出吗？")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)

            # 添加"记住选择"复选框
            remember_checkbox = QCheckBox("记住我的选择，不再提示")
            msg_box.setCheckBox(remember_checkbox)

            # 应用主题样式
            msg_box.setStyleSheet(get_stylesheet("dialog"))

            result = msg_box.exec_()

            # 保存用户选择
            if remember_checkbox.isChecked():
                self.confirm_exit_with_connections = (result == QMessageBox.Yes)
                self.config_service.set('confirm_exit_with_connections', self.confirm_exit_with_connections)
                self.config_service.save()

            if result == QMessageBox.No:
                event.ignore()
                return
        elif open_tabs_count > 0 and not self.confirm_exit_with_connections:
            # 用户之前选择了"否"并记住选择
            event.ignore()
            return

        # 关闭所有连接
        self.connection_manager.close_all_connections()
        event.accept()
