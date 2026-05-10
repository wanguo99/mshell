"""设置对话框"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QWidget, QLabel, QSpinBox, QCheckBox, QComboBox,
                             QPushButton, QGroupBox, QFormLayout, QDialogButtonBox)
from PyQt5.QtCore import Qt

from ui.theme import Theme, get_stylesheet


class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self, config_service, parent=None):
        super().__init__(parent)
        self.config_service = config_service
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("设置")
        self.setMinimumSize(600, 500)
        self.setStyleSheet(get_stylesheet("dialog"))

        layout = QVBoxLayout(self)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(get_stylesheet("tabwidget"))

        # 终端设置
        self.terminal_tab = self._create_terminal_tab()
        self.tab_widget.addTab(self.terminal_tab, "终端")

        # 行为设置
        self.behavior_tab = self._create_behavior_tab()
        self.tab_widget.addTab(self.behavior_tab, "行为")

        # 外观设置
        self.appearance_tab = self._create_appearance_tab()
        self.tab_widget.addTab(self.appearance_tab, "外观")

        layout.addWidget(self.tab_widget)

        # 按钮区域
        button_layout = QHBoxLayout()

        # 恢复默认配置按钮
        self.reset_button = QPushButton("恢复默认配置")
        self.reset_button.setStyleSheet(get_stylesheet("button"))
        self.reset_button.clicked.connect(self.reset_to_default)
        button_layout.addWidget(self.reset_button)

        button_layout.addStretch()

        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        button_box.button(QDialogButtonBox.Ok).setStyleSheet(get_stylesheet("button_primary"))
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(get_stylesheet("button"))
        button_box.button(QDialogButtonBox.Apply).setStyleSheet(get_stylesheet("button"))
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply_settings)
        button_layout.addWidget(button_box)

        layout.addLayout(button_layout)

    def _create_terminal_tab(self):
        """创建终端设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 缓冲区设置
        buffer_group = QGroupBox("缓冲区")
        buffer_layout = QFormLayout(buffer_group)

        self.scrollback_spin = QSpinBox()
        self.scrollback_spin.setRange(100, 100000)
        self.scrollback_spin.setSingleStep(1000)
        self.scrollback_spin.setSuffix(" 行")
        buffer_layout.addRow("滚动缓冲区大小:", self.scrollback_spin)

        layout.addWidget(buffer_group)

        # 字体设置
        font_group = QGroupBox("字体")
        font_layout = QFormLayout(font_group)

        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems([
            "Monospace", "Consolas", "Courier New",
            "DejaVu Sans Mono", "Menlo", "Monaco"
        ])
        font_layout.addRow("字体:", self.font_family_combo)

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setSuffix(" pt")
        font_layout.addRow("字体大小:", self.font_size_spin)

        layout.addWidget(font_group)

        # 颜色方案
        color_group = QGroupBox("颜色方案")
        color_layout = QFormLayout(color_group)

        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems([
            "default", "solarized_dark", "monokai", "dracula"
        ])
        color_layout.addRow("颜色方案:", self.color_scheme_combo)

        layout.addWidget(color_group)

        layout.addStretch()
        return widget

    def _create_behavior_tab(self):
        """创建行为设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 连接行为
        connection_group = QGroupBox("连接行为")
        connection_layout = QVBoxLayout(connection_group)

        self.auto_close_check = QCheckBox("连接断开时自动关闭标签页")
        connection_layout.addWidget(self.auto_close_check)

        self.confirm_exit_check = QCheckBox("退出时确认关闭活动连接")
        connection_layout.addWidget(self.confirm_exit_check)

        self.replace_welcome_check = QCheckBox("打开新连接后替换欢迎页")
        connection_layout.addWidget(self.replace_welcome_check)

        layout.addWidget(connection_group)

        # 会话行为
        session_group = QGroupBox("会话")
        session_layout = QVBoxLayout(session_group)

        self.restore_session_check = QCheckBox("启动时恢复上次会话")
        session_layout.addWidget(self.restore_session_check)

        layout.addWidget(session_group)

        layout.addStretch()
        return widget

    def _create_appearance_tab(self):
        """创建外观设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 主题设置
        theme_group = QGroupBox("主题")
        theme_layout = QFormLayout(theme_group)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["深色", "浅色"])
        theme_layout.addRow("应用主题:", self.theme_combo)

        layout.addWidget(theme_group)

        # 侧边栏设置
        sidebar_group = QGroupBox("侧边栏")
        sidebar_layout = QVBoxLayout(sidebar_group)

        self.show_sidebar_check = QCheckBox("显示侧边栏")
        self.show_sidebar_check.setChecked(True)
        sidebar_layout.addWidget(self.show_sidebar_check)

        layout.addWidget(sidebar_group)

        layout.addStretch()
        return widget

    def load_settings(self):
        """加载当前设置"""
        # 终端设置
        terminal_config = self.config_service.get('terminal', {})
        self.scrollback_spin.setValue(terminal_config.get('scrollback_lines', 10000))
        self.font_family_combo.setCurrentText(terminal_config.get('font_family', 'Monospace'))
        self.font_size_spin.setValue(terminal_config.get('font_size', 12))
        self.color_scheme_combo.setCurrentText(terminal_config.get('color_scheme', 'default'))

        # 行为设置
        auto_close = self.config_service.get_auto_close_on_disconnect()
        if auto_close is not None:
            self.auto_close_check.setChecked(auto_close)
        else:
            self.auto_close_check.setTristate(True)
            self.auto_close_check.setCheckState(Qt.PartiallyChecked)

        confirm_exit = self.config_service.get('confirm_exit_with_connections')
        if confirm_exit is not None:
            self.confirm_exit_check.setChecked(confirm_exit)
        else:
            self.confirm_exit_check.setTristate(True)
            self.confirm_exit_check.setCheckState(Qt.PartiallyChecked)

        self.restore_session_check.setChecked(
            self.config_service.get('application', {}).get('restore_session', False)
        )

        self.replace_welcome_check.setChecked(
            self.config_service.get('application', {}).get('replace_welcome_page', False)
        )

        # 外观设置
        theme = self.config_service.get('application', {}).get('theme', 'dark')
        self.theme_combo.setCurrentIndex(0 if theme == 'dark' else 1)

        show_sidebar = self.config_service.get('ui', {}).get('show_sidebar', True)
        self.show_sidebar_check.setChecked(show_sidebar)

    def apply_settings(self):
        """应用设置"""
        # 终端设置
        terminal_config = {
            'scrollback_lines': self.scrollback_spin.value(),
            'font_family': self.font_family_combo.currentText(),
            'font_size': self.font_size_spin.value(),
            'color_scheme': self.color_scheme_combo.currentText()
        }
        self.config_service.set('terminal', terminal_config)

        # 行为设置
        if self.auto_close_check.checkState() != Qt.PartiallyChecked:
            self.config_service.set_auto_close_on_disconnect(self.auto_close_check.isChecked())

        if self.confirm_exit_check.checkState() != Qt.PartiallyChecked:
            self.config_service.set('confirm_exit_with_connections', self.confirm_exit_check.isChecked())

        application_config = self.config_service.get('application', {})
        application_config['restore_session'] = self.restore_session_check.isChecked()
        application_config['replace_welcome_page'] = self.replace_welcome_check.isChecked()

        # 保存主题设置
        theme_index = self.theme_combo.currentIndex()
        application_config['theme'] = 'dark' if theme_index == 0 else 'light'

        self.config_service.set('application', application_config)

        # 保存侧边栏设置
        ui_config = self.config_service.get('ui', {})
        ui_config['show_sidebar'] = self.show_sidebar_check.isChecked()
        self.config_service.set('ui', ui_config)

        # 保存配置
        self.config_service.save()

    def accept(self):
        """确定按钮"""
        self.apply_settings()
        super().accept()

    def reset_to_default(self):
        """恢复默认配置"""
        from PyQt5.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self,
            '确认恢复默认配置',
            '确定要恢复所有设置为默认值吗？\n此操作将清除所有自定义配置（包括已保存的连接）。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # 恢复默认配置
            self.config_service._config_manager.reset_to_default()
            # 重新加载设置到界面
            self.load_settings()
            QMessageBox.information(
                self,
                '恢复成功',
                '配置已恢复为默认值。'
            )
