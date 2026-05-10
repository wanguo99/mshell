"""终端显示组件

基于PyQt5的终端显示组件，支持ANSI颜色渲染、键盘输入、滚动历史等功能。
"""

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QKeyEvent, QTextCursor

from tests.mock_platform import get_mock_platform
from terminal.ansi_parser import AnsiParser, AnsiToken
from terminal.color_scheme import ColorSchemeManager


class TerminalWidget(QTextEdit):
    """终端显示组件"""

    # 信号：发送数据到连接
    data_to_send = pyqtSignal(bytes)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 使用mock platform (Day 5会切换到真实接口)
        self.platform = get_mock_platform()

        # 初始化ANSI解析器和颜色方案
        self.ansi_parser = AnsiParser()
        self.color_scheme_manager = ColorSchemeManager()

        # 设置终端属性
        self._setup_terminal()

        # 输入缓冲区
        self._input_buffer = ""

    def _setup_terminal(self):
        """设置终端属性"""
        # 设置为只读模式（通过keyPressEvent处理输入）
        self.setReadOnly(False)

        # 设置默认字体
        font_family, font_size = self.platform.ui.get_default_font()
        self.set_font(font_family, font_size)

        # 设置颜色方案
        self.set_color_scheme("default")

        # 设置滚动行数
        self.document().setMaximumBlockCount(10000)

        # 禁用自动换行（可选）
        self.setLineWrapMode(QTextEdit.WidgetWidth)

        # 设置光标样式
        self.setCursorWidth(8)

    def write_output(self, data: str):
        """写入输出到终端

        Args:
            data: 要显示的文本数据
        """
        if not data:
            return

        # 解析ANSI序列
        tokens = self.ansi_parser.parse(data)

        # 移动光标到末尾
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)

        # 渲染每个token
        for token in tokens:
            self._render_token(cursor, token)

        # 自动滚动到底部
        self.ensureCursorVisible()

    def _render_token(self, cursor: QTextCursor, token: AnsiToken):
        """渲染单个token

        Args:
            cursor: 文本光标
            token: ANSI token
        """
        # 创建字符格式
        char_format = QTextCharFormat()

        # 设置前景色
        if token.style.fg_color:
            r, g, b = token.style.fg_color
            char_format.setForeground(QColor(r, g, b))
        else:
            scheme = self.color_scheme_manager.get_current_scheme()
            r, g, b = scheme.get_foreground()
            char_format.setForeground(QColor(r, g, b))

        # 设置背景色
        if token.style.bg_color:
            r, g, b = token.style.bg_color
            char_format.setBackground(QColor(r, g, b))

        # 设置文本样式
        if token.style.bold:
            char_format.setFontWeight(QFont.Bold)
        if token.style.italic:
            char_format.setFontItalic(True)
        if token.style.underline:
            char_format.setFontUnderline(True)

        # 反显效果
        if token.style.reverse:
            fg = char_format.foreground().color()
            bg = char_format.background().color()
            char_format.setForeground(bg)
            char_format.setBackground(fg)

        # 插入文本
        cursor.insertText(token.text, char_format)

    def keyPressEvent(self, event: QKeyEvent):
        """处理键盘输入

        Args:
            event: 键盘事件
        """
        key = event.key()
        modifiers = event.modifiers()
        text = event.text()

        # 处理特殊键
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            # 回车键
            self.data_to_send.emit(b'\n')
            self._input_buffer = ""
        elif key == Qt.Key_Backspace:
            # 退格键
            if self._input_buffer:
                self._input_buffer = self._input_buffer[:-1]
                self.data_to_send.emit(b'\x7f')  # DEL字符
        elif key == Qt.Key_Tab:
            # Tab键
            self.data_to_send.emit(b'\t')
        elif key == Qt.Key_Up:
            # 上方向键
            self.data_to_send.emit(b'\x1b[A')
        elif key == Qt.Key_Down:
            # 下方向键
            self.data_to_send.emit(b'\x1b[B')
        elif key == Qt.Key_Right:
            # 右方向键
            self.data_to_send.emit(b'\x1b[C')
        elif key == Qt.Key_Left:
            # 左方向键
            self.data_to_send.emit(b'\x1b[D')
        elif key == Qt.Key_Home:
            # Home键
            self.data_to_send.emit(b'\x1b[H')
        elif key == Qt.Key_End:
            # End键
            self.data_to_send.emit(b'\x1b[F')
        elif key == Qt.Key_PageUp:
            # PageUp键
            self.data_to_send.emit(b'\x1b[5~')
        elif key == Qt.Key_PageDown:
            # PageDown键
            self.data_to_send.emit(b'\x1b[6~')
        elif key == Qt.Key_Delete:
            # Delete键
            self.data_to_send.emit(b'\x1b[3~')
        elif modifiers & Qt.ControlModifier:
            # Ctrl组合键
            if key == Qt.Key_C:
                self.data_to_send.emit(b'\x03')  # Ctrl+C
            elif key == Qt.Key_D:
                self.data_to_send.emit(b'\x04')  # Ctrl+D
            elif key == Qt.Key_Z:
                self.data_to_send.emit(b'\x1a')  # Ctrl+Z
            elif key == Qt.Key_L:
                self.clear()  # Ctrl+L 清屏
        elif text:
            # 普通字符
            try:
                data = text.encode('utf-8')
                self._input_buffer += text
                self.data_to_send.emit(data)
            except UnicodeEncodeError:
                pass

    def clear(self):
        """清空终端"""
        self.document().clear()
        self.ansi_parser.reset()
        self._input_buffer = ""

    def set_font(self, font_family: str, font_size: int):
        """设置字体

        Args:
            font_family: 字体名称
            font_size: 字体大小
        """
        font = QFont(font_family, font_size)
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        self.setFont(font)

    def set_color_scheme(self, scheme_name: str):
        """设置颜色方案

        Args:
            scheme_name: 颜色方案名称
        """
        try:
            self.color_scheme_manager.set_current_scheme(scheme_name)
            scheme = self.color_scheme_manager.get_current_scheme()

            # 设置背景色和前景色
            bg = scheme.get_background()
            fg = scheme.get_foreground()

            palette = self.palette()
            palette.setColor(palette.Base, QColor(*bg))
            palette.setColor(palette.Text, QColor(*fg))
            self.setPalette(palette)

            # 设置样式表
            self.setStyleSheet(f"""
                QTextEdit {{
                    background-color: rgb({bg[0]}, {bg[1]}, {bg[2]});
                    color: rgb({fg[0]}, {fg[1]}, {fg[2]});
                    border: none;
                }}
            """)
        except KeyError as e:
            print(f"Warning: {e}")

    def get_available_color_schemes(self) -> list:
        """获取可用的颜色方案列表

        Returns:
            颜色方案名称列表
        """
        return self.color_scheme_manager.list_schemes()

    def set_scrollback_lines(self, lines: int):
        """设置滚动历史行数

        Args:
            lines: 最大行数
        """
        self.document().setMaximumBlockCount(lines)
