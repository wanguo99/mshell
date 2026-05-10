"""快捷指令执行器单元测试"""

import pytest
from core.command_executor import CommandExecutor
from core.connection_manager import ConnectionManager


class MockConnection(ConnectionManager):
    """Mock连接用于测试"""

    def __init__(self):
        super().__init__()
        self.sent_data = []
        self._connected = True

    def connect(self, **kwargs) -> bool:
        self._connected = True
        return True

    def disconnect(self):
        self._connected = False

    def send(self, data: bytes):
        self.sent_data.append(data)

    def is_connected(self) -> bool:
        return self._connected


class TestCommandExecutor:
    """测试快捷指令执行器"""

    def test_simple_command(self):
        """测试简单指令"""
        executor = CommandExecutor()
        conn = MockConnection()

        executor.execute("ls -la", conn)

        assert len(conn.sent_data) == 1
        assert conn.sent_data[0] == b"ls -la\n"

    def test_variable_replacement(self):
        """测试变量替换"""
        executor = CommandExecutor()
        conn = MockConnection()

        variables = {"user": "root", "host": "192.168.1.1"}
        executor.execute("ssh {user}@{host}", conn, variables)

        assert len(conn.sent_data) == 1
        assert conn.sent_data[0] == b"ssh root@192.168.1.1\n"

    def test_global_variables(self):
        """测试全局变量"""
        executor = CommandExecutor()
        conn = MockConnection()

        executor.set_variable("user", "admin")
        executor.execute("echo {user}", conn)

        assert conn.sent_data[0] == b"echo admin\n"

    def test_variable_override(self):
        """测试变量覆盖"""
        executor = CommandExecutor()
        conn = MockConnection()

        executor.set_variable("user", "admin")
        executor.execute("echo {user}", conn, {"user": "root"})

        assert conn.sent_data[0] == b"echo root\n"

    def test_missing_variable(self):
        """测试缺失变量"""
        executor = CommandExecutor()
        conn = MockConnection()

        executor.execute("echo {missing}", conn)

        assert conn.sent_data[0] == b"echo {missing}\n"

    def test_not_connected(self):
        """测试未连接时执行"""
        executor = CommandExecutor()
        conn = MockConnection()
        conn.disconnect()

        executor.execute("ls", conn)

        assert len(conn.sent_data) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
