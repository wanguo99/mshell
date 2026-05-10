"""终端引擎 - 协调缓冲区和渲染器

核心优化：
1. 按需渲染：只在有数据时渲染，不使用定时器
2. 脏行渲染：只重绘变化的行
3. 渲染器抽象：支持不同的渲染后端
"""

from typing import Protocol
from .buffer import TerminalBuffer, Cell


class IRenderer(Protocol):
    """渲染器接口

    定义渲染器必须实现的方法。
    """

    def render_line(self, row: int, cells: list) -> None:
        """渲染一行

        Args:
            row: 行号
            cells: 单元格列表
        """
        ...

    def render_cursor(self, row: int, col: int) -> None:
        """渲染光标

        Args:
            row: 光标行号
            col: 光标列号
        """
        ...

    def append_history_line(self, cells: list) -> None:
        """追加历史行

        Args:
            cells: 单元格列表
        """
        ...

    def clear_screen(self) -> None:
        """清空屏幕"""
        ...

    def scroll_to_bottom(self) -> None:
        """滚动到底部"""
        ...


class TerminalEngine:
    """终端引擎

    协调终端缓冲区和渲染器，实现高性能终端渲染。
    """

    def __init__(self, renderer: IRenderer, rows: int = 24, cols: int = 80, history: int = 10000):
        """初始化终端引擎

        Args:
            renderer: 渲染器实现
            rows: 终端行数
            cols: 终端列数
            history: 历史缓冲区行数
        """
        self.buffer = TerminalBuffer(rows, cols, history)
        self.renderer = renderer
        self.render_pending = False

    def write(self, data: str) -> None:
        """写入数据到终端

        Args:
            data: 文本数据
        """
        self.buffer.feed(data)
        self.render_pending = True

    def render(self) -> None:
        """渲染终端（仅渲染脏行）"""
        if not self.render_pending:
            return

        # 处理新增的历史行
        new_history_lines = self.buffer.get_new_history_lines()
        for cells in new_history_lines:
            self.renderer.append_history_line(cells)

        # 全屏重绘或脏行渲染
        if self.buffer.full_redraw:
            # 全屏重绘
            for row in range(self.buffer.rows):
                cells = self.buffer.get_line(row)
                self.renderer.render_line(row, cells)
        else:
            # 仅渲染脏行
            dirty_lines = self.buffer.get_dirty_lines()
            for row in dirty_lines:
                cells = self.buffer.get_line(row)
                self.renderer.render_line(row, cells)

        # 渲染光标
        cursor_row, cursor_col = self.buffer.get_cursor_position()
        self.renderer.render_cursor(cursor_row, cursor_col)

        # 滚动到底部
        self.renderer.scroll_to_bottom()

        # 清除脏行标记
        self.buffer.clear_dirty()
        self.render_pending = False

    def resize(self, rows: int, cols: int) -> None:
        """调整终端大小

        Args:
            rows: 新的行数
            cols: 新的列数
        """
        self.buffer.resize(rows, cols)
        self.render_pending = True

    def clear(self) -> None:
        """清空终端"""
        self.buffer.clear()
        self.renderer.clear_screen()
        self.render_pending = False

    def get_buffer(self) -> TerminalBuffer:
        """获取终端缓冲区

        Returns:
            终端缓冲区实例
        """
        return self.buffer
