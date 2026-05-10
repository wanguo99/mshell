"""ANSI解析器单元测试"""

import pytest
from terminal.ansi_parser import AnsiParser, AnsiStyle


class TestAnsiParser:
    """测试ANSI解析器"""

    def test_plain_text(self):
        """测试纯文本解析"""
        parser = AnsiParser()
        tokens = parser.parse("Hello World")

        assert len(tokens) == 1
        assert tokens[0].text == "Hello World"
        assert tokens[0].style.fg_color is None
        assert tokens[0].style.bold is False

    def test_basic_color(self):
        """测试基本颜色解析"""
        parser = AnsiParser()
        tokens = parser.parse("\x1b[31mRed Text\x1b[0m")

        assert len(tokens) == 1
        assert tokens[0].text == "Red Text"
        assert tokens[0].style.fg_color == (205, 0, 0)

    def test_bold_text(self):
        """测试粗体文本"""
        parser = AnsiParser()
        tokens = parser.parse("\x1b[1mBold\x1b[0m")

        assert len(tokens) == 1
        assert tokens[0].text == "Bold"
        assert tokens[0].style.bold is True

    def test_multiple_styles(self):
        """测试多种样式组合"""
        parser = AnsiParser()
        tokens = parser.parse("\x1b[1;31;4mBold Red Underline\x1b[0m")

        assert len(tokens) == 1
        assert tokens[0].text == "Bold Red Underline"
        assert tokens[0].style.bold is True
        assert tokens[0].style.underline is True
        assert tokens[0].style.fg_color == (205, 0, 0)

    def test_256_color(self):
        """测试256色模式"""
        parser = AnsiParser()
        tokens = parser.parse("\x1b[38;5;196mRed 256\x1b[0m")

        assert len(tokens) == 1
        assert tokens[0].text == "Red 256"
        assert tokens[0].style.fg_color is not None

    def test_rgb_color(self):
        """测试RGB颜色"""
        parser = AnsiParser()
        tokens = parser.parse("\x1b[38;2;255;128;0mOrange\x1b[0m")

        assert len(tokens) == 1
        assert tokens[0].text == "Orange"
        assert tokens[0].style.fg_color == (255, 128, 0)

    def test_background_color(self):
        """测试背景色"""
        parser = AnsiParser()
        tokens = parser.parse("\x1b[41mRed BG\x1b[0m")

        assert len(tokens) == 1
        assert tokens[0].text == "Red BG"
        assert tokens[0].style.bg_color == (205, 0, 0)

    def test_mixed_text(self):
        """测试混合文本"""
        parser = AnsiParser()
        tokens = parser.parse("Plain \x1b[31mRed\x1b[0m Plain")

        assert len(tokens) == 3
        assert tokens[0].text == "Plain "
        assert tokens[1].text == "Red"
        assert tokens[2].text == " Plain"
        assert tokens[1].style.fg_color == (205, 0, 0)

    def test_cursor_position(self):
        """测试光标位置"""
        parser = AnsiParser()
        parser.parse("\x1b[10;20H")

        row, col = parser.get_cursor_position()
        assert row == 9  # 0-indexed
        assert col == 19

    def test_reset(self):
        """测试重置"""
        parser = AnsiParser()
        parser.parse("\x1b[1;31mBold Red")
        parser.reset()

        assert parser.current_style.bold is False
        assert parser.current_style.fg_color is None
        row, col = parser.get_cursor_position()
        assert row == 0
        assert col == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
