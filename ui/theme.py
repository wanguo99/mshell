"""UI主题配色方案

定义统一的颜色变量，确保整体UI风格一致
"""


class Theme:
    """深色主题配色方案（参考Xshell）"""

    # 主色调
    PRIMARY_BG = "#1e1e1e"          # 主背景色（更深）
    SECONDARY_BG = "#252526"        # 次要背景色
    TERTIARY_BG = "#2d2d30"         # 第三背景色

    # 侧边栏
    SIDEBAR_BG = "#252526"          # 侧边栏背景
    SIDEBAR_HEADER_BG = "#2d2d30"   # 侧边栏标题背景
    SIDEBAR_BORDER = "#3e3e42"      # 侧边栏边框

    # 文字颜色
    TEXT_PRIMARY = "#cccccc"        # 主要文字
    TEXT_SECONDARY = "#969696"      # 次要文字
    TEXT_DISABLED = "#656565"       # 禁用文字
    TEXT_HIGHLIGHT = "#ffffff"      # 高亮文字

    # 边框和分隔线
    BORDER_LIGHT = "#3e3e42"        # 浅色边框
    BORDER_DARK = "#2d2d30"         # 深色边框
    DIVIDER = "#3e3e42"             # 分隔线

    # 交互状态
    HOVER_BG = "#2a2d2e"            # 悬停背景
    ACTIVE_BG = "#37373d"           # 激活背景
    SELECTED_BG = "#094771"         # 选中背景（蓝色调）
    PRESSED_BG = "#0e639c"          # 按下背景

    # 按钮
    BUTTON_BG = "#2d2d30"           # 按钮背景
    BUTTON_HOVER = "#37373d"        # 按钮悬停
    BUTTON_PRESSED = "#094771"      # 按钮按下
    BUTTON_PRIMARY = "#0e639c"      # 主要按钮
    BUTTON_PRIMARY_HOVER = "#1177bb" # 主要按钮悬停

    # 标签页
    TAB_BG = "#2d2d30"              # 标签背景
    TAB_ACTIVE_BG = "#1e1e1e"       # 激活标签背景
    TAB_HOVER_BG = "#37373d"        # 标签悬停
    TAB_BORDER = "#3e3e42"          # 标签边框

    # 终端
    TERMINAL_BG = "#1e1e1e"         # 终端背景
    TERMINAL_FG = "#cccccc"         # 终端前景
    TERMINAL_CURSOR = "#ffffff"     # 终端光标

    # 状态颜色
    SUCCESS = "#4ec9b0"             # 成功（青色）
    WARNING = "#ce9178"             # 警告（橙色）
    ERROR = "#f48771"               # 错误（红色）
    INFO = "#4fc1ff"                # 信息（蓝色）

    # 阴影
    SHADOW_LIGHT = "rgba(0, 0, 0, 0.1)"
    SHADOW_MEDIUM = "rgba(0, 0, 0, 0.2)"
    SHADOW_HEAVY = "rgba(0, 0, 0, 0.3)"

    # 圆角
    RADIUS_SMALL = "2px"
    RADIUS_MEDIUM = "4px"
    RADIUS_LARGE = "6px"

    # 间距
    SPACING_XS = "2px"
    SPACING_SM = "4px"
    SPACING_MD = "8px"
    SPACING_LG = "12px"
    SPACING_XL = "16px"


class LightTheme:
    """浅色主题配色方案"""

    # 主色调
    PRIMARY_BG = "#ffffff"          # 主背景色
    SECONDARY_BG = "#f3f3f3"        # 次要背景色
    TERTIARY_BG = "#e8e8e8"         # 第三背景色

    # 侧边栏
    SIDEBAR_BG = "#f3f3f3"          # 侧边栏背景
    SIDEBAR_HEADER_BG = "#e8e8e8"   # 侧边栏标题背景
    SIDEBAR_BORDER = "#d0d0d0"      # 侧边栏边框

    # 文字颜色
    TEXT_PRIMARY = "#333333"        # 主要文字
    TEXT_SECONDARY = "#666666"      # 次要文字
    TEXT_DISABLED = "#999999"       # 禁用文字
    TEXT_HIGHLIGHT = "#000000"      # 高亮文字

    # 边框和分隔线
    BORDER_LIGHT = "#d0d0d0"        # 浅色边框
    BORDER_DARK = "#c0c0c0"         # 深色边框
    DIVIDER = "#d0d0d0"             # 分隔线

    # 交互状态
    HOVER_BG = "#e0e0e0"            # 悬停背景
    ACTIVE_BG = "#d8d8d8"           # 激活背景
    SELECTED_BG = "#0078d4"         # 选中背景（蓝色调）
    PRESSED_BG = "#005a9e"          # 按下背景

    # 按钮
    BUTTON_BG = "#e8e8e8"           # 按钮背景
    BUTTON_HOVER = "#d8d8d8"        # 按钮悬停
    BUTTON_PRESSED = "#0078d4"      # 按钮按下
    BUTTON_PRIMARY = "#0078d4"      # 主要按钮
    BUTTON_PRIMARY_HOVER = "#106ebe" # 主要按钮悬停

    # 标签页
    TAB_BG = "#e8e8e8"              # 标签背景
    TAB_ACTIVE_BG = "#ffffff"       # 激活标签背景
    TAB_HOVER_BG = "#d8d8d8"        # 标签悬停
    TAB_BORDER = "#d0d0d0"          # 标签边框

    # 终端
    TERMINAL_BG = "#ffffff"         # 终端背景
    TERMINAL_FG = "#333333"         # 终端前景
    TERMINAL_CURSOR = "#000000"     # 终端光标

    # 状态颜色
    SUCCESS = "#107c10"             # 成功（绿色）
    WARNING = "#ff8c00"             # 警告（橙色）
    ERROR = "#e81123"               # 错误（红色）
    INFO = "#0078d4"                # 信息（蓝色）

    # 阴影
    SHADOW_LIGHT = "rgba(0, 0, 0, 0.05)"
    SHADOW_MEDIUM = "rgba(0, 0, 0, 0.1)"
    SHADOW_HEAVY = "rgba(0, 0, 0, 0.15)"

    # 圆角
    RADIUS_SMALL = "2px"
    RADIUS_MEDIUM = "4px"
    RADIUS_LARGE = "6px"

    # 间距
    SPACING_XS = "2px"
    SPACING_SM = "4px"
    SPACING_MD = "8px"
    SPACING_LG = "12px"
    SPACING_XL = "16px"


# 当前主题（默认深色）
_current_theme = Theme


def set_theme(theme_name: str):
    """设置当前主题

    Args:
        theme_name: 主题名称 ('dark' 或 'light')
    """
    global _current_theme
    if theme_name == 'light':
        _current_theme = LightTheme
    else:
        _current_theme = Theme


def get_current_theme():
    """获取当前主题"""
    return _current_theme


def get_stylesheet(component: str) -> str:
    """获取组件样式表

    Args:
        component: 组件名称

    Returns:
        CSS样式字符串
    """
    # 使用当前主题
    theme = _current_theme

    stylesheets = {
        "sidebar": f"""
            QWidget {{
                background-color: {theme.SIDEBAR_BG};
                border-right: 1px solid {theme.SIDEBAR_BORDER};
            }}
        """,

        "sidebar_title": f"""
            QLabel {{
                background-color: {theme.SIDEBAR_HEADER_BG};
                color: {theme.TEXT_PRIMARY};
                padding: {theme.SPACING_MD} {theme.SPACING_LG};
                font-size: 13px;
                font-weight: bold;
                border-bottom: 1px solid {theme.BORDER_LIGHT};
            }}
        """,

        "connection_list": f"""
            QListWidget {{
                background-color: {theme.SIDEBAR_BG};
                border: none;
                outline: none;
                color: {theme.TEXT_PRIMARY};
                font-size: 12px;
            }}
            QListWidget::item {{
                padding: {theme.SPACING_MD} {theme.SPACING_LG};
                border-bottom: 1px solid {theme.BORDER_DARK};
            }}
            QListWidget::item:hover {{
                background-color: {theme.HOVER_BG};
            }}
            QListWidget::item:selected {{
                background-color: {theme.SELECTED_BG};
                color: {theme.TEXT_HIGHLIGHT};
            }}
        """,

        "button": f"""
            QPushButton {{
                background-color: {theme.BUTTON_BG};
                color: {theme.TEXT_PRIMARY};
                border: none;
                outline: none;
                padding: {theme.SPACING_MD} {theme.SPACING_LG};
                border-radius: {theme.RADIUS_SMALL};
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {theme.BUTTON_HOVER};
                color: {theme.TEXT_HIGHLIGHT};
            }}
            QPushButton:pressed {{
                background-color: {theme.BUTTON_PRESSED};
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """,

        "button_primary": f"""
            QPushButton {{
                background-color: {theme.BUTTON_PRIMARY};
                color: {theme.TEXT_HIGHLIGHT};
                border: none;
                outline: none;
                padding: {theme.SPACING_MD} {theme.SPACING_LG};
                border-radius: {theme.RADIUS_SMALL};
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme.BUTTON_PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {theme.PRESSED_BG};
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """,

        "menubar": f"""
            QMenuBar {{
                background-color: {theme.SECONDARY_BG};
                color: {theme.TEXT_PRIMARY};
                border-bottom: 1px solid {theme.BORDER_LIGHT};
                padding: {theme.SPACING_XS};
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: {theme.SPACING_SM} {theme.SPACING_LG};
                border-radius: {theme.RADIUS_SMALL};
            }}
            QMenuBar::item:selected {{
                background-color: {theme.HOVER_BG};
            }}
            QMenuBar::item:pressed {{
                background-color: {theme.ACTIVE_BG};
            }}
            QMenu {{
                background-color: {theme.SECONDARY_BG};
                color: {theme.TEXT_PRIMARY};
                border: 1px solid {theme.BORDER_LIGHT};
                border-radius: {theme.RADIUS_SMALL};
            }}
            QMenu::item {{
                padding: {theme.SPACING_MD} {theme.SPACING_XL};
            }}
            QMenu::item:selected {{
                background-color: {theme.SELECTED_BG};
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {theme.BORDER_LIGHT};
                margin: {theme.SPACING_XS} 0px;
            }}
        """,

        "tabwidget": f"""
            QTabWidget::pane {{
                border: 1px solid {theme.TAB_BORDER};
                background-color: {theme.TERMINAL_BG};
                top: -1px;
            }}
            QTabBar {{
                background-color: {theme.TAB_BG};
            }}
            QTabBar::tab {{
                background-color: {theme.TAB_BG};
                color: {theme.TEXT_SECONDARY};
                border: 1px solid {theme.TAB_BORDER};
                border-bottom: none;
                padding: {theme.SPACING_MD} {theme.SPACING_XL};
                margin-right: {theme.SPACING_XS};
                border-top-left-radius: {theme.RADIUS_MEDIUM};
                border-top-right-radius: {theme.RADIUS_MEDIUM};
            }}
            QTabBar::tab:selected {{
                background-color: {theme.TAB_ACTIVE_BG};
                color: {theme.TEXT_HIGHLIGHT};
                border-bottom: 1px solid {theme.TAB_ACTIVE_BG};
            }}
            QTabBar::tab:hover {{
                background-color: {theme.TAB_HOVER_BG};
                color: {theme.TEXT_PRIMARY};
            }}
        """,

        "context_menu": f"""
            QMenu {{
                background-color: {theme.SECONDARY_BG};
                color: {theme.TEXT_PRIMARY};
                border: 1px solid {theme.BORDER_LIGHT};
                border-radius: {theme.RADIUS_SMALL};
            }}
            QMenu::item {{
                padding: {theme.SPACING_MD} {theme.SPACING_XL};
            }}
            QMenu::item:selected {{
                background-color: {theme.SELECTED_BG};
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {theme.BORDER_LIGHT};
                margin: {theme.SPACING_XS} 0px;
            }}
        """,

        "dialog": f"""
            QDialog {{
                background-color: {theme.SECONDARY_BG};
                color: {theme.TEXT_PRIMARY};
            }}
            QLabel {{
                color: {theme.TEXT_PRIMARY};
            }}
            QLineEdit, QSpinBox, QComboBox {{
                background-color: {theme.TERTIARY_BG};
                color: {theme.TEXT_PRIMARY};
                border: 1px solid {theme.BORDER_LIGHT};
                border-radius: {theme.RADIUS_SMALL};
                padding: {theme.SPACING_SM} {theme.SPACING_MD};
            }}
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
                border: 1px solid {theme.SELECTED_BG};
            }}
            QCheckBox {{
                color: {theme.TEXT_PRIMARY};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {theme.BORDER_LIGHT};
                border-radius: {theme.RADIUS_SMALL};
                background-color: {theme.TERTIARY_BG};
            }}
            QCheckBox::indicator:checked {{
                background-color: {theme.BUTTON_PRIMARY};
                border: 1px solid {theme.BUTTON_PRIMARY};
            }}
            QGroupBox {{
                color: {theme.TEXT_PRIMARY};
                border: 1px solid {theme.BORDER_LIGHT};
                border-radius: {theme.RADIUS_SMALL};
                margin-top: 12px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: {theme.TEXT_HIGHLIGHT};
            }}
        """
    }

    return stylesheets.get(component, "")
