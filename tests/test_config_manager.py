"""测试配置管理器"""
import pytest
import tempfile
from pathlib import Path
from config.config_manager import ConfigManager


def test_config_manager_init():
    """测试配置管理器初始化"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        assert manager is not None


def test_config_load_default():
    """测试加载默认配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        manager.load()

        connections = manager.get_connections()
        assert isinstance(connections, list)


def test_config_get_set():
    """测试配置读写"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        manager.load()

        manager.set('test.key', 'test_value')
        value = manager.get('test.key')
        assert value == 'test_value'

        default_value = manager.get('nonexistent.key', 'default')
        assert default_value == 'default'


def test_config_connections():
    """测试连接配置管理"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        manager.load()

        test_conn = {
            'name': 'test_ssh',
            'type': 'ssh',
            'host': '192.168.1.1',
            'port': 22,
            'username': 'test'
        }

        manager.add_connection(test_conn)
        connections = manager.get_connections()
        assert any(c['name'] == 'test_ssh' for c in connections)

        result = manager.remove_connection('test_ssh')
        assert result is True

        connections = manager.get_connections()
        assert not any(c['name'] == 'test_ssh' for c in connections)


def test_config_shortcuts():
    """测试快捷键配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        manager.load()

        manager.set_shortcut('Ctrl+X', 'test_action')
        shortcuts = manager.get_shortcuts()
        assert shortcuts.get('Ctrl+X') == 'test_action'


def test_config_quick_commands():
    """测试快捷指令配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        manager.load()

        test_cmd = {
            'name': 'test_command',
            'command': 'echo test',
            'shortcut': 'F10'
        }

        manager.add_quick_command(test_cmd)
        commands = manager.get_quick_commands()
        assert any(c['name'] == 'test_command' for c in commands)


def test_config_terminal_settings():
    """测试终端设置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        manager.load()

        terminal_settings = manager.get_terminal_settings()
        assert isinstance(terminal_settings, dict)


def test_config_color_schemes():
    """测试颜色方案"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        manager.load()

        schemes = manager.get_color_schemes()
        assert isinstance(schemes, dict)

        default_scheme = manager.get_color_scheme('default')
        if default_scheme:
            assert 'background' in default_scheme
            assert 'foreground' in default_scheme


def test_config_save_load():
    """测试配置保存和加载"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'

        manager1 = ConfigManager(str(config_file))
        manager1.load()
        manager1.set('test.value', 12345)
        manager1.save()

        manager2 = ConfigManager(str(config_file))
        manager2.load()
        value = manager2.get('test.value')
        assert value == 12345


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
