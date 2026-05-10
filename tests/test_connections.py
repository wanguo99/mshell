"""SSH连接单元测试"""

import pytest
import time
from core.ssh_connection import SSHConnection


class TestSSHConnection:
    """测试SSH连接"""

    def test_connection_creation(self):
        """测试创建SSH连接对象"""
        ssh = SSHConnection()
        assert ssh is not None
        assert not ssh.is_connected()

    def test_connection_callbacks(self):
        """测试连接回调"""
        ssh = SSHConnection()

        data_received = []
        connection_states = []

        ssh.on_data_received = lambda data: data_received.append(data)
        ssh.on_connection_changed = lambda state: connection_states.append(state)

        # 触发回调
        ssh._notify_data_received(b"test")
        ssh._notify_connection_changed(True)

        assert len(data_received) == 1
        assert data_received[0] == b"test"
        assert len(connection_states) == 1
        assert connection_states[0] is True

    def test_disconnect_when_not_connected(self):
        """测试未连接时断开"""
        ssh = SSHConnection()
        ssh.disconnect()  # 不应该抛出异常
        assert not ssh.is_connected()


class TestSerialConnection:
    """测试串口连接"""

    def test_list_ports(self):
        """测试列出串口"""
        from core.serial_connection import SerialConnection
        ports = SerialConnection.list_available_ports()
        assert isinstance(ports, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
