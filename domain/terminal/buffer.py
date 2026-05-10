"""终端缓冲区 - 使用脏行标记优化渲染性能

核心优化：
1. 脏行标记：只重绘变化的行
2. 双缓冲：避免渲染撕裂
3. 按需刷新：数据到达时才渲染，不使用定时器
"""

import pyte
from typing import Set, List
from dataclasses import dataclass


@dataclass
class Cell:
    """终端单元格"""
    char: str
    fg_color: tuple = None
    bg_color: tuple = None
    bold: bool = False
    italic: bool = False
    underline: bool = False
    reverse: bool = False


class TerminalBuffer:
    """终端缓冲区

    使用 pyte 作为底层解析器，添加脏行标记优化。
    """

    def __init__(self, rows: int = 24, cols: int = 80, history: int = 10000):
        """初始化终端缓冲区

        Args:
            rows: 终端行数
            cols: 终端列数
            history: 历史缓冲区行数
        """
        self.rows = rows
        self.cols = cols
        self.history_size = history

        # 使用 pyte 作为底层终端模拟器
        self.screen = pyte.HistoryScreen(cols, rows, history=history)
        self.stream = pyte.Stream(self.screen)

        # 脏行标记（记录哪些行需要重绘）
        self.dirty_lines: Set[int] = set()
        self.full_redraw = True  # 首次渲染需要全屏重绘

        # 历史行追踪
        self.last_history_length = 0

    def feed(self, data: str) -> None:
        """喂入数据到终端

        Args:
            data: 文本数据（可能包含 ANSI 转义序列）
        """
        # 记录喂入前的状态
        old_cursor_y = self.screen.cursor.y

        # 喂入数据到 pyte
        self.stream.feed(data)

        # 标记脏行
        self._mark_dirty_lines(old_cursor_y)

    def _mark_dirty_lines(self, old_cursor_y: int) -> None:
        """标记脏行

        Args:
            old_cursor_y: 喂入数据前的光标行
        """
        # 简化策略：标记光标所在行及其附近的行为脏行
        # 更精确的策略需要对比前后缓冲区内容
        current_cursor_y = self.screen.cursor.y

        # 标记光标移动范围内的所有行
        start_line = min(old_cursor_y, current_cursor_y)
        end_line = max(old_cursor_y, current_cursor_y)

        for line in range(max(0, start_line), min(self.rows, end_line + 1)):
            self.dirty_lines.add(line)

        # 如果有新的历史行，标记需要追加
        current_history_length = len(self.screen.history.top)
        if current_history_length > self.last_history_length:
            # 有新历史行，需要特殊处理
            self.full_redraw = True

    def get_dirty_lines(self) -> Set[int]:
        """获取脏行集合

        Returns:
            脏行行号集合
        """
        return self.dirty_lines.copy()

    def clear_dirty(self) -> None:
        """清除脏行标记"""
        self.dirty_lines.clear()
        self.full_redraw = False

    def get_line(self, row: int) -> List[Cell]:
        """获取指定行的内容

        Args:
            row: 行号（0-based）

        Returns:
            单元格列表
        """
        if row < 0 or row >= self.rows:
            return []

        line = self.screen.buffer[row]
        cells = []

        for col in range(self.cols):
            char = line[col]
            cell = Cell(
                char=char.data,
                fg_color=self._convert_color(char.fg) if char.fg != 'default' else None,
                bg_color=self._convert_color(char.bg) if char.bg != 'default' else None,
                bold=char.bold,
                italic=char.italics,
                underline=char.underscore,
                reverse=char.reverse
            )
            cells.append(cell)

        return cells

    def get_cursor_position(self) -> tuple:
        """获取光标位置

        Returns:
            (row, col) 元组
        """
        return (self.screen.cursor.y, self.screen.cursor.x)

    def get_new_history_lines(self) -> List[List[Cell]]:
        """获取新增的历史行

        Returns:
            新增历史行的单元格列表
        """
        current_history_length = len(self.screen.history.top)
        new_lines = []

        if current_history_length > self.last_history_length:
            for i in range(self.last_history_length, current_history_length):
                if i < len(self.screen.history.top):
                    line = self.screen.history.top[i]
                    cells = []

                    # 遍历列（使用 cols 而不是直接迭代 line）
                    for col in range(self.cols):
                        char = line[col]

                        # 处理 Char 对象
                        if hasattr(char, 'data'):
                            cell = Cell(
                                char=char.data,
                                fg_color=self._convert_color(char.fg) if char.fg != 'default' else None,
                                bg_color=self._convert_color(char.bg) if char.bg != 'default' else None,
                                bold=char.bold,
                                italic=char.italics,
                                underline=char.underscore,
                                reverse=char.reverse
                            )
                        elif isinstance(char, str):
                            cell = Cell(
                                char=char,
                                fg_color=None,
                                bg_color=None,
                                bold=False,
                                italic=False,
                                underline=False,
                                reverse=False
                            )
                        else:
                            # 默认空格
                            cell = Cell(
                                char=' ',
                                fg_color=None,
                                bg_color=None,
                                bold=False,
                                italic=False,
                                underline=False,
                                reverse=False
                            )
                        cells.append(cell)
                    new_lines.append(cells)

            self.last_history_length = current_history_length

        return new_lines

    def resize(self, rows: int, cols: int) -> None:
        """调整终端大小

        Args:
            rows: 新的行数
            cols: 新的列数
        """
        self.rows = rows
        self.cols = cols
        self.screen.resize(rows, cols)
        self.full_redraw = True

    def clear(self) -> None:
        """清空终端（保留历史）"""
        # 不使用 reset()，而是使用 erase_in_display(2) 来清屏
        # 这样会保留历史缓冲区
        self.screen.erase_in_display(2)
        self.screen.cursor_position(0, 0)
        self.dirty_lines.clear()
        self.full_redraw = True

    def _convert_color(self, color) -> tuple:
        """转换 pyte 颜色为 RGB 元组

        Args:
            color: pyte 颜色（字符串或整数）

        Returns:
            RGB 元组
        """
        # 标准 16 色映射
        color_map = {
            'black': (0, 0, 0),
            'red': (205, 0, 0),
            'green': (0, 205, 0),
            'brown': (205, 205, 0),
            'blue': (0, 0, 238),
            'magenta': (205, 0, 205),
            'cyan': (0, 205, 205),
            'white': (229, 229, 229),
            'brightblack': (127, 127, 127),
            'brightred': (255, 0, 0),
            'brightgreen': (0, 255, 0),
            'brightyellow': (255, 255, 0),
            'brightblue': (92, 92, 255),
            'brightmagenta': (255, 0, 255),
            'brightcyan': (0, 255, 255),
            'brightwhite': (255, 255, 255),
        }

        if isinstance(color, str):
            return color_map.get(color, (229, 229, 229))
        elif isinstance(color, int):
            return self._convert_256_to_rgb(color)
        else:
            return (229, 229, 229)

    def _convert_256_to_rgb(self, color_index: int) -> tuple:
        """转换 256 色索引为 RGB

        Args:
            color_index: 0-255 的颜色索引

        Returns:
            RGB 元组
        """
        if color_index < 16:
            # 标准 16 色
            standard = [
                (0, 0, 0), (205, 0, 0), (0, 205, 0), (205, 205, 0),
                (0, 0, 238), (205, 0, 205), (0, 205, 205), (229, 229, 229),
                (127, 127, 127), (255, 0, 0), (0, 255, 0), (255, 255, 0),
                (92, 92, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)
            ]
            return standard[color_index]
        elif color_index < 232:
            # 216 色立方体
            index = color_index - 16
            r = (index // 36) * 51
            g = ((index % 36) // 6) * 51
            b = (index % 6) * 51
            return (r, g, b)
        else:
            # 24 级灰度
            gray = 8 + (color_index - 232) * 10
            return (gray, gray, gray)
