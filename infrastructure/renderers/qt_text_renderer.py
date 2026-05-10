"""Qt 渲染器 - 使用 QTextEdit 渲染终端

优化版本：
1. 只渲染脏行，不重绘整个屏幕
2. 按需刷新，不使用定时器
3. 实现 IRenderer 接口，可替换
"""

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QTextCursor
from PyQt5.QtCore import Qt
from domain.terminal.buffer import Cell


class QtTextRenderer:
    """Qt 文本渲染器

    使用 QTextEdit 渲染终端内容。
    """

    def __init__(self, text_edit: QTextEdit, rows: int = 24, cols: int = 80):
        """初始化渲染器

        Args:
            text_edit: QTextEdit 组件
            rows: 终端行数
            cols: 终端列数
        """
        self.text_edit = text_edit
        self.rows = rows
        self.cols = cols

        # 默认颜色
        self.default_fg = QColor(229, 229, 229)
        self.default_bg = QColor(0, 0, 0)

        # 历史行计数
        self.history_line_count = 0

        # 初始化文档结构（预分配行）
        self._init_document()

    def _init_document(self) -> None:
        """初始化文档结构"""
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start)

        # 预分配行
        for i in range(self.rows):
            if i > 0:
                cursor.insertText('\n')
            cursor.insertText(' ' * self.cols)

    def render_line(self, row: int, cells: list) -> None:
        """渲染一行

        Args:
            row: 行号（相对于可见区域）
            cells: 单元格列表
        """
        if row < 0 or row >= self.rows:
            return

        cursor = self.text_edit.textCursor()

        # 计算实际行号（历史行 + 可见行）
        actual_row = self.history_line_count + row

        # 移动到指定行
        cursor.movePosition(QTextCursor.Start)
        for _ in range(actual_row):
            cursor.movePosition(QTextCursor.Down)

        # 选择整行
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)

        # 删除旧内容
        cursor.removeSelectedText()

        # 渲染新内容
        for cell in cells[:self.cols]:  # 限制列数
            char_format = self._create_format(cell)
            cursor.insertText(cell.char, char_format)

    def render_cursor(self, row: int, col: int) -> None:
        """渲染光标

        Args:
            row: 光标行号
            col: 光标列号
        """
        # Qt 的 QTextEdit 自带光标，这里可以选择性地高亮光标位置
        # 简化实现：不做额外处理
        pass

    def append_history_line(self, cells: list) -> None:
        """追加历史行

        Args:
            cells: 单元格列表
        """
        cursor = self.text_edit.textCursor()

        # 移动到文档开头
        cursor.movePosition(QTextCursor.Start)

        # 如果已有历史行，移动到历史区域末尾
        if self.history_line_count > 0:
            for _ in range(self.history_line_count):
                cursor.movePosition(QTextCursor.Down)

        # 插入历史行内容
        for cell in cells:
            char_format = self._create_format(cell)
            cursor.insertText(cell.char, char_format)

        # 在历史行后面插入换行符（分隔历史行和可见区域）
        cursor.insertText('\n')

        # 增加历史行计数
        self.history_line_count += 1

        # 如果用户在底部，自动滚动到底部
        scrollbar = self.text_edit.verticalScrollBar()
        was_at_bottom = scrollbar.value() >= scrollbar.maximum() - 10

        if was_at_bottom:
            self.scroll_to_bottom()

    def clear_screen(self) -> None:
        """清空屏幕"""
        self.text_edit.clear()
        self.history_line_count = 0
        self._init_document()

    def scroll_to_bottom(self) -> None:
        """滚动到底部"""
        scrollbar = self.text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _create_format(self, cell: Cell) -> QTextCharFormat:
        """创建字符格式

        Args:
            cell: 单元格

        Returns:
            QTextCharFormat 对象
        """
        char_format = QTextCharFormat()

        # 设置前景色
        if cell.fg_color:
            char_format.setForeground(QColor(*cell.fg_color))
        else:
            char_format.setForeground(self.default_fg)

        # 设置背景色
        if cell.bg_color:
            char_format.setBackground(QColor(*cell.bg_color))

        # 设置文本样式
        if cell.bold:
            char_format.setFontWeight(QFont.Bold)
        if cell.italic:
            char_format.setFontItalic(True)
        if cell.underline:
            char_format.setFontUnderline(True)

        # 反显
        if cell.reverse:
            fg = char_format.foreground().color()
            bg = char_format.background().color()
            char_format.setForeground(bg)
            char_format.setBackground(fg)

        return char_format
