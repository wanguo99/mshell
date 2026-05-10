"""ANSI转义序列解析器

解析终端输出中的ANSI转义序列，包括颜色、文本样式、光标控制等。
"""

import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class AnsiStyle:
    """ANSI样式"""
    fg_color: Optional[Tuple[int, int, int]] = None  # RGB前景色
    bg_color: Optional[Tuple[int, int, int]] = None  # RGB背景色
    bold: bool = False
    italic: bool = False
    underline: bool = False
    blink: bool = False
    reverse: bool = False


@dataclass
class AnsiToken:
    """ANSI解析后的token"""
    text: str
    style: AnsiStyle


class AnsiParser:
    """ANSI转义序列解析器"""

    # ANSI转义序列正则表达式
    ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[([0-9;]*)([A-Za-z])')

    # 标准16色映射 (30-37, 40-47)
    STANDARD_COLORS = {
        0: (0, 0, 0),        # 黑色
        1: (205, 0, 0),      # 红色
        2: (0, 205, 0),      # 绿色
        3: (205, 205, 0),    # 黄色
        4: (0, 0, 238),      # 蓝色
        5: (205, 0, 205),    # 品红
        6: (0, 205, 205),    # 青色
        7: (229, 229, 229),  # 白色
    }

    # 高亮16色映射 (90-97, 100-107)
    BRIGHT_COLORS = {
        0: (127, 127, 127),  # 亮黑色(灰色)
        1: (255, 0, 0),      # 亮红色
        2: (0, 255, 0),      # 亮绿色
        3: (255, 255, 0),    # 亮黄色
        4: (92, 92, 255),    # 亮蓝色
        5: (255, 0, 255),    # 亮品红
        6: (0, 255, 255),    # 亮青色
        7: (255, 255, 255),  # 亮白色
    }

    def __init__(self):
        self.current_style = AnsiStyle()
        self.cursor_row = 0
        self.cursor_col = 0

    def parse(self, text: str) -> List[AnsiToken]:
        """解析文本中的ANSI序列

        Args:
            text: 包含ANSI序列的文本

        Returns:
            解析后的token列表
        """
        tokens = []
        last_pos = 0

        for match in self.ANSI_ESCAPE_PATTERN.finditer(text):
            # 添加转义序列之前的文本
            if match.start() > last_pos:
                plain_text = text[last_pos:match.start()]
                if plain_text:
                    tokens.append(AnsiToken(plain_text, self._copy_style()))

            # 处理ANSI序列
            params = match.group(1)
            command = match.group(2)
            self._process_ansi_sequence(params, command)

            last_pos = match.end()

        # 添加剩余文本
        if last_pos < len(text):
            remaining = text[last_pos:]
            if remaining:
                tokens.append(AnsiToken(remaining, self._copy_style()))

        return tokens

    def _process_ansi_sequence(self, params: str, command: str):
        """处理ANSI转义序列

        Args:
            params: 参数字符串 (如 "1;31")
            command: 命令字符 (如 "m")
        """
        if command == 'm':  # SGR (Select Graphic Rendition)
            self._process_sgr(params)
        elif command in 'ABCD':  # 光标移动
            self._process_cursor_move(params, command)
        elif command in 'HF':  # 光标定位
            self._process_cursor_position(params)
        elif command == 'J':  # 清屏
            self._process_erase_display(params)
        elif command == 'K':  # 清行
            self._process_erase_line(params)

    def _process_sgr(self, params: str):
        """处理SGR (Select Graphic Rendition) 序列

        Args:
            params: SGR参数字符串
        """
        if not params:
            params = "0"

        param_list = [int(p) if p else 0 for p in params.split(';')]
        i = 0

        while i < len(param_list):
            code = param_list[i]

            if code == 0:  # 重置所有属性
                self.current_style = AnsiStyle()
            elif code == 1:  # 粗体
                self.current_style.bold = True
            elif code == 3:  # 斜体
                self.current_style.italic = True
            elif code == 4:  # 下划线
                self.current_style.underline = True
            elif code == 5:  # 闪烁
                self.current_style.blink = True
            elif code == 7:  # 反显
                self.current_style.reverse = True
            elif code == 22:  # 取消粗体
                self.current_style.bold = False
            elif code == 23:  # 取消斜体
                self.current_style.italic = False
            elif code == 24:  # 取消下划线
                self.current_style.underline = False
            elif code == 25:  # 取消闪烁
                self.current_style.blink = False
            elif code == 27:  # 取消反显
                self.current_style.reverse = False
            elif 30 <= code <= 37:  # 标准前景色
                self.current_style.fg_color = self.STANDARD_COLORS[code - 30]
            elif code == 38:  # 扩展前景色
                i = self._process_extended_color(param_list, i, is_foreground=True)
            elif code == 39:  # 默认前景色
                self.current_style.fg_color = None
            elif 40 <= code <= 47:  # 标准背景色
                self.current_style.bg_color = self.STANDARD_COLORS[code - 40]
            elif code == 48:  # 扩展背景色
                i = self._process_extended_color(param_list, i, is_foreground=False)
            elif code == 49:  # 默认背景色
                self.current_style.bg_color = None
            elif 90 <= code <= 97:  # 高亮前景色
                self.current_style.fg_color = self.BRIGHT_COLORS[code - 90]
            elif 100 <= code <= 107:  # 高亮背景色
                self.current_style.bg_color = self.BRIGHT_COLORS[code - 100]

            i += 1

    def _process_extended_color(self, param_list: List[int], index: int, is_foreground: bool) -> int:
        """处理扩展颜色 (256色或RGB)

        Args:
            param_list: 参数列表
            index: 当前索引 (指向38或48)
            is_foreground: 是否为前景色

        Returns:
            处理后的索引位置
        """
        if index + 1 >= len(param_list):
            return index

        color_type = param_list[index + 1]

        if color_type == 5:  # 256色模式
            if index + 2 < len(param_list):
                color_index = param_list[index + 2]
                rgb = self._convert_256_to_rgb(color_index)
                if is_foreground:
                    self.current_style.fg_color = rgb
                else:
                    self.current_style.bg_color = rgb
                return index + 2
        elif color_type == 2:  # RGB模式
            if index + 4 < len(param_list):
                r = param_list[index + 2]
                g = param_list[index + 3]
                b = param_list[index + 4]
                if is_foreground:
                    self.current_style.fg_color = (r, g, b)
                else:
                    self.current_style.bg_color = (r, g, b)
                return index + 4

        return index + 1

    def _convert_256_to_rgb(self, color_index: int) -> Tuple[int, int, int]:
        """将256色索引转换为RGB

        Args:
            color_index: 0-255的颜色索引

        Returns:
            RGB元组
        """
        if color_index < 16:
            # 标准16色
            if color_index < 8:
                return self.STANDARD_COLORS[color_index]
            else:
                return self.BRIGHT_COLORS[color_index - 8]
        elif color_index < 232:
            # 216色立方体 (16-231)
            index = color_index - 16
            r = (index // 36) * 51
            g = ((index % 36) // 6) * 51
            b = (index % 6) * 51
            return (r, g, b)
        else:
            # 24级灰度 (232-255)
            gray = 8 + (color_index - 232) * 10
            return (gray, gray, gray)

    def _process_cursor_move(self, params: str, command: str):
        """处理光标移动命令

        Args:
            params: 参数字符串
            command: 命令字符 (A/B/C/D)
        """
        n = int(params) if params else 1

        if command == 'A':  # CUU - 光标上移
            self.cursor_row = max(0, self.cursor_row - n)
        elif command == 'B':  # CUD - 光标下移
            self.cursor_row += n
        elif command == 'C':  # CUF - 光标右移
            self.cursor_col += n
        elif command == 'D':  # CUB - 光标左移
            self.cursor_col = max(0, self.cursor_col - n)

    def _process_cursor_position(self, params: str):
        """处理光标定位命令

        Args:
            params: 参数字符串 (如 "10;20")
        """
        if not params:
            self.cursor_row = 0
            self.cursor_col = 0
            return

        parts = params.split(';')
        if len(parts) >= 1:
            self.cursor_row = int(parts[0]) - 1 if parts[0] else 0
        if len(parts) >= 2:
            self.cursor_col = int(parts[1]) - 1 if parts[1] else 0

    def _process_erase_display(self, params: str):
        """处理清屏命令

        Args:
            params: 参数字符串
        """
        n = int(params) if params else 0
        # 0: 清除从光标到屏幕末尾
        # 1: 清除从屏幕开始到光标
        # 2: 清除整个屏幕
        # 3: 清除整个屏幕及回滚缓冲区
        pass

    def _process_erase_line(self, params: str):
        """处理清行命令

        Args:
            params: 参数字符串
        """
        n = int(params) if params else 0
        # 0: 清除从光标到行尾
        # 1: 清除从行首到光标
        # 2: 清除整行
        pass

    def _copy_style(self) -> AnsiStyle:
        """复制当前样式

        Returns:
            样式副本
        """
        return AnsiStyle(
            fg_color=self.current_style.fg_color,
            bg_color=self.current_style.bg_color,
            bold=self.current_style.bold,
            italic=self.current_style.italic,
            underline=self.current_style.underline,
            blink=self.current_style.blink,
            reverse=self.current_style.reverse
        )

    def reset(self):
        """重置解析器状态"""
        self.current_style = AnsiStyle()
        self.cursor_row = 0
        self.cursor_col = 0

    def get_cursor_position(self) -> Tuple[int, int]:
        """获取当前光标位置

        Returns:
            (行, 列) 元组
        """
        return (self.cursor_row, self.cursor_col)
