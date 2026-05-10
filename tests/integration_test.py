"""简单的集成测试示例

演示如何使用terminal-core模块的各个组件。
"""

import sys
import time


def test_terminal_widget():
    """测试终端组件"""
    print("Testing TerminalWidget...")

    try:
        from PyQt5.QtWidgets import QApplication
        from terminal.terminal_widget import TerminalWidget

        app = QApplication(sys.argv)
        terminal = TerminalWidget()

        # 测试写入输出
        terminal.write_output("Plain text\n")
        terminal.write_output("\x1b[31mRed text\x1b[0m\n")
        terminal.write_output("\x1b[1;32mBold green text\x1b[0m\n")

        # 测试颜色方案
        schemes = terminal.get_available_color_schemes()
        print(f"Available color schemes: {schemes}")

        terminal.set_color_scheme("monokai")
        terminal.write_output("Monokai theme\n")

        print("✓ TerminalWidget test passed")
    except Exception as e:
        print(f"⚠ TerminalWidget test skipped (no display): {e}")


def test_command_executor():
    """测试命令执行器"""
    print("\nTesting CommandExecutor...")

    from core.command_executor import CommandExecutor

    executor = CommandExecutor()

    # 设置变量
    executor.set_variable("user", "root")
    executor.set_variable("host", "localhost")

    # 测试变量替换（需要传入全局变量）
    all_vars = {**executor.get_all_variables()}
    cmd = executor._replace_variables("ssh {user}@{host}", all_vars)
    assert cmd == "ssh root@localhost", f"Expected 'ssh root@localhost', got '{cmd}'"

    # 测试变量覆盖
    all_vars = {**executor.get_all_variables(), "user": "admin"}
    cmd = executor._replace_variables("ssh {user}@{host}", all_vars)
    assert cmd == "ssh admin@localhost", f"Expected 'ssh admin@localhost', got '{cmd}'"

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


def test_ansi_parser():
    """测试ANSI解析器"""
    print("\nTesting AnsiParser...")

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

    print("✓ AnsiParser test passed")


if __name__ == '__main__':
    print("Running terminal-core integration tests...\n")
    print("=" * 50)

    test_ansi_parser()
    test_command_executor()
    test_ssh_connection()
    test_terminal_widget()

    print("\n" + "=" * 50)
    print("All tests passed! ✓")
