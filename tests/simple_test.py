"""简单测试脚本，验证平台适配层和配置管理器"""
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from mshell_platform.factory import get_platform
from config.config_manager import ConfigManager


def test_platform():
    """测试平台适配层"""
    print("=" * 60)
    print("测试平台适配层")
    print("=" * 60)

    platform = get_platform()
    print(f"✓ 成功获取平台实例")

    # 测试串口接口
    ports = platform.serial.get_available_ports()
    print(f"✓ 串口列表: {ports}")

    # 测试配置路径接口
    config_dir = platform.config.get_config_dir()
    print(f"✓ 配置目录: {config_dir}")

    data_dir = platform.config.get_data_dir()
    print(f"✓ 数据目录: {data_dir}")

    cache_dir = platform.config.get_cache_dir()
    print(f"✓ 缓存目录: {cache_dir}")

    # 测试文件系统接口
    home_dir = platform.filesystem.get_home_dir()
    print(f"✓ 主目录: {home_dir}")

    separator = platform.filesystem.get_path_separator()
    print(f"✓ 路径分隔符: {repr(separator)}")

    # 测试UI接口
    font_name, font_size = platform.ui.get_default_font()
    print(f"✓ 默认字体: {font_name} {font_size}pt")

    fonts = platform.ui.get_available_fonts()
    print(f"✓ 可用字体: {', '.join(fonts[:3])}...")

    modifier = platform.ui.get_shortcut_modifier()
    print(f"✓ 快捷键修饰符: {modifier}")

    line_ending = platform.ui.get_line_ending()
    print(f"✓ 行尾符: {repr(line_ending)}")

    theme = platform.ui.get_theme()
    print(f"✓ 系统主题: {theme}")

    # 测试剪贴板接口
    try:
        test_text = "MShell Test"
        platform.clipboard.set_text(test_text)
        result = platform.clipboard.get_text()
        if result == test_text:
            print(f"✓ 剪贴板测试通过")
        else:
            print(f"⚠ 剪贴板测试失败: 期望 '{test_text}', 得到 '{result}'")
        platform.clipboard.clear()
    except Exception as e:
        print(f"⚠ 剪贴板测试跳过: {e}")

    print()


def test_config_manager():
    """测试配置管理器"""
    print("=" * 60)
    print("测试配置管理器")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'test_config.yaml'
        manager = ConfigManager(str(config_file))
        print(f"✓ 创建配置管理器")

        manager.load()
        print(f"✓ 加载配置")

        # 测试基本读写
        manager.set('test.key', 'test_value')
        value = manager.get('test.key')
        assert value == 'test_value', f"期望 'test_value', 得到 '{value}'"
        print(f"✓ 配置读写测试通过")

        # 测试连接配置
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
        print(f"✓ 添加连接配置")

        result = manager.remove_connection('test_ssh')
        assert result is True
        print(f"✓ 删除连接配置")

        # 测试快捷键
        manager.set_shortcut('Ctrl+X', 'test_action')
        shortcuts = manager.get_shortcuts()
        assert shortcuts.get('Ctrl+X') == 'test_action'
        print(f"✓ 快捷键配置")

        # 测试快捷指令
        test_cmd = {
            'name': 'test_command',
            'command': 'echo test',
            'shortcut': 'F10'
        }
        manager.add_quick_command(test_cmd)
        commands = manager.get_quick_commands()
        assert any(c['name'] == 'test_command' for c in commands)
        print(f"✓ 快捷指令配置")

        # 测试保存和加载
        manager.set('test.value', 12345)
        manager.save()
        print(f"✓ 保存配置")

        manager2 = ConfigManager(str(config_file))
        manager2.load()
        value = manager2.get('test.value')
        assert value == 12345
        print(f"✓ 重新加载配置")

        # 测试终端设置
        terminal_settings = manager.get_terminal_settings()
        print(f"✓ 终端设置: {len(terminal_settings)} 项")

        # 测试颜色方案
        schemes = manager.get_color_schemes()
        print(f"✓ 颜色方案: {len(schemes)} 个")

    print()


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("MShell 平台适配层测试")
    print("=" * 60 + "\n")

    try:
        test_platform()
        test_config_manager()

        print("=" * 60)
        print("✓ 所有测试通过!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
