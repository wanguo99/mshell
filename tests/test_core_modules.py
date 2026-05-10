"""非GUI集成测试

在无显示环境下测试terminal-core模块的核心功能。
"""


def test_ansi_parser():
    """测试ANSI解析器"""
    print("Testing AnsiParser...")

    from terminal.ansi_parser import AnsiParser

    parser = AnsiParser()

    # 测试基本颜色
    tokens = parser.parse("\x1b[31mRed\x1b[0m")
    assert len(tokens) == 1, "Should have 1 token"
    assert tokens[0].text == "Red", "Text should be 'Red'"
    assert tokens[0].style.fg_color == (205, 0, 0), "Color should be red"

    # 测试RGB颜色
    parser.reset()
    tokens = parser.parse("\x1b[38;2;255;128;0mOrange\x1b[0m")
    assert tokens[0].style.fg_color == (255, 128, 0), "Color should be orange"

    # 测试粗体
    parser.reset()
    tokens = parser.parse("\x1b[1mBold\x1b[0m")
    assert tokens[0].style.bold is True, "Should be bold"

    # 测试混合样式
    parser.reset()
    tokens = parser.parse("Plain \x1b[31mRed\x1b[0m Plain")
    assert len(tokens) == 3, "Should have 3 tokens"
    assert tokens[1].style.fg_color == (205, 0, 0), "Middle token should be red"

    print("✓ AnsiParser test passed")


def test_command_executor():
    """测试命令执行器"""
    print("\nTesting CommandExecutor...")

    from core.command_executor import CommandExecutor

    executor = CommandExecutor()

    # 设置变量
    executor.set_variable("user", "root")
    executor.set_variable("host", "localhost")

    # 测试变量替换
    all_vars = {**executor.get_all_variables()}
    cmd = executor._replace_variables("ssh {user}@{host}", all_vars)
    assert cmd == "ssh root@localhost", f"Expected 'ssh root@localhost', got '{cmd}'"

    # 测试变量覆盖
    all_vars = {**executor.get_all_variables(), "user": "admin"}
    cmd = executor._replace_variables("ssh {user}@{host}", all_vars)
    assert cmd == "ssh admin@localhost", f"Expected 'ssh admin@localhost', got '{cmd}'"

    # 测试缺失变量
    cmd = executor._replace_variables("echo {missing}", {})
    assert cmd == "echo {missing}", "Missing variable should remain unchanged"

    print("✓ CommandExecutor test passed")


def test_ssh_connection():
    """测试SSH连接（不实际连接）"""
    print("\nTesting SSHConnection...")

    from core.ssh_connection import SSHConnection

    ssh = SSHConnection()

    # 测试初始状态
    assert not ssh.is_connected(), "SSH should not be connected initially"

    # 测试回调
    data_received = []
    connection_states = []

    ssh.on_data_received = lambda data: data_received.append(data)
    ssh.on_connection_changed = lambda state: connection_states.append(state)

    # 触发回调
    ssh._notify_data_received(b"test data")
    ssh._notify_connection_changed(True)

    assert len(data_received) == 1, "Should receive one data callback"
    assert data_received[0] == b"test data", "Data should match"
    assert len(connection_states) == 1, "Should receive one state callback"
    assert connection_states[0] is True, "State should be True"

    print("✓ SSHConnection test passed")


def test_serial_connection():
    """测试串口连接"""
    print("\nTesting SerialConnection...")

    from core.serial_connection import SerialConnection

    serial = SerialConnection()

    # 测试初始状态
    assert not serial.is_connected(), "Serial should not be connected initially"

    # 测试列出串口
    ports = SerialConnection.list_available_ports()
    assert isinstance(ports, list), "Should return a list"
    print(f"  Found {len(ports)} serial ports")

    print("✓ SerialConnection test passed")


def test_color_scheme():
    """测试颜色方案"""
    print("\nTesting ColorScheme...")

    from terminal.color_scheme import ColorSchemeManager

    manager = ColorSchemeManager()

    # 测试列出方案
    schemes = manager.list_schemes()
    assert "default" in schemes, "Should have default scheme"
    assert "monokai" in schemes, "Should have monokai scheme"
    assert "solarized_dark" in schemes, "Should have solarized_dark scheme"

    # 测试获取方案
    default_scheme = manager.get_scheme("default")
    assert default_scheme.name == "default", "Scheme name should match"
    assert default_scheme.get_background() == (0, 0, 0), "Default background should be black"

    # 测试切换方案
    manager.set_current_scheme("monokai")
    current = manager.get_current_scheme()
    assert current.name == "monokai", "Current scheme should be monokai"

    print("✓ ColorScheme test passed")


if __name__ == '__main__':
    print("Running terminal-core integration tests (non-GUI)...\n")
    print("=" * 50)

    test_ansi_parser()
    test_command_executor()
    test_ssh_connection()
    test_serial_connection()
    test_color_scheme()

    print("\n" + "=" * 50)
    print("All tests passed! ✓")
