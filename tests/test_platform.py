"""测试平台适配层"""
import pytest
from mshell_platform.factory import get_platform


def test_get_platform():
    """测试获取平台实例"""
    platform = get_platform()
    assert platform is not None
    assert platform.serial is not None
    assert platform.config is not None
    assert platform.clipboard is not None
    assert platform.filesystem is not None
    assert platform.ui is not None


def test_serial_interface():
    """测试串口接口"""
    platform = get_platform()
    ports = platform.serial.get_available_ports()
    assert isinstance(ports, list)

    if ports:
        desc = platform.serial.get_port_description(ports[0])
        assert isinstance(desc, str)


def test_config_interface():
    """测试配置路径接口"""
    platform = get_platform()

    config_dir = platform.config.get_config_dir()
    assert config_dir.exists()

    data_dir = platform.config.get_data_dir()
    assert data_dir.exists()

    cache_dir = platform.config.get_cache_dir()
    assert cache_dir.exists()


def test_clipboard_interface():
    """测试剪贴板接口"""
    platform = get_platform()

    test_text = "Hello, MShell!"
    platform.clipboard.set_text(test_text)
    result = platform.clipboard.get_text()
    assert result == test_text

    platform.clipboard.clear()
    result = platform.clipboard.get_text()
    assert result == ""


def test_filesystem_interface():
    """测试文件系统接口"""
    platform = get_platform()

    home_dir = platform.filesystem.get_home_dir()
    assert home_dir.exists()

    separator = platform.filesystem.get_path_separator()
    assert separator in ['/', '\\']

    normalized = platform.filesystem.normalize_path("/tmp/test")
    assert isinstance(normalized, str)


def test_ui_interface():
    """测试UI接口"""
    platform = get_platform()

    font_name, font_size = platform.ui.get_default_font()
    assert isinstance(font_name, str)
    assert isinstance(font_size, int)
    assert font_size > 0

    fonts = platform.ui.get_available_fonts()
    assert isinstance(fonts, list)
    assert len(fonts) > 0

    modifier = platform.ui.get_shortcut_modifier()
    assert modifier in ['Ctrl', 'Cmd']

    line_ending = platform.ui.get_line_ending()
    assert line_ending in ['\n', '\r\n']

    theme = platform.ui.get_theme()
    assert theme in ['light', 'dark']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
