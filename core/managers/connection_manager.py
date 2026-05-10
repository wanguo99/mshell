"""连接管理器，负责管理所有连接会话"""

from typing import Dict, Optional, List
from PyQt5.QtCore import QObject, pyqtSignal

from models.connection import ConnectionConfig, SSHConnectionConfig, SerialConnectionConfig
from models.session import Session
from connection.ssh_connection import SSHConnection
from connection.serial_connection import SerialConnection
from terminal.terminal_widget import TerminalWidget


class ConnectionManager(QObject):
    """连接管理器"""

    # 信号定义
    connection_created = pyqtSignal(Session)  # 连接创建成功
    connection_closed = pyqtSignal(int)  # 连接关闭（tab_index）
    connection_error = pyqtSignal(str)  # 连接错误

    def __init__(self):
        super().__init__()
        self._sessions: Dict[int, Session] = {}  # tab_index -> Session
        self._next_tab_index = 0

    def create_ssh_connection(self, config: SSHConnectionConfig, terminal: TerminalWidget) -> Optional[Session]:
        """创建SSH连接

        Args:
            config: SSH连接配置
            terminal: 终端widget

        Returns:
            Session对象，失败返回None
        """
        try:
            # 创建SSH连接
            ssh_conn = SSHConnection(
                host=config.host,
                port=config.port,
                username=config.username,
                password=config.password,
                key_file=config.key_file
            )

            # 连接信号
            ssh_conn.data_received.connect(terminal.append_data)
            ssh_conn.connection_closed.connect(lambda: self._on_connection_closed(self._next_tab_index))
            terminal.data_to_send.connect(ssh_conn.send)

            # 建立连接
            if not ssh_conn.connect():
                self.connection_error.emit(f"SSH连接失败: {config.host}")
                return None

            # 创建会话
            session = Session(
                tab_index=self._next_tab_index,
                config=config,
                connection=ssh_conn,
                terminal=terminal
            )

            self._sessions[self._next_tab_index] = session
            self._next_tab_index += 1

            self.connection_created.emit(session)
            return session

        except Exception as e:
            self.connection_error.emit(f"创建SSH连接失败: {str(e)}")
            return None

    def create_serial_connection(self, config: SerialConnectionConfig, terminal: TerminalWidget) -> Optional[Session]:
        """创建串口连接

        Args:
            config: 串口连接配置
            terminal: 终端widget

        Returns:
            Session对象，失败返回None
        """
        try:
            # 创建串口连接
            serial_conn = SerialConnection(
                port=config.port,
                baudrate=config.baudrate,
                bytesize=config.bytesize,
                parity=config.parity,
                stopbits=config.stopbits
            )

            # 连接信号
            serial_conn.data_received.connect(terminal.append_data)
            serial_conn.connection_closed.connect(lambda: self._on_connection_closed(self._next_tab_index))
            terminal.data_to_send.connect(serial_conn.send)

            # 建立连接
            if not serial_conn.connect():
                self.connection_error.emit(f"串口连接失败: {config.port}")
                return None

            # 创建会话
            session = Session(
                tab_index=self._next_tab_index,
                config=config,
                connection=serial_conn,
                terminal=terminal
            )

            self._sessions[self._next_tab_index] = session
            self._next_tab_index += 1

            self.connection_created.emit(session)
            return session

        except Exception as e:
            self.connection_error.emit(f"创建串口连接失败: {str(e)}")
            return None

    def close_connection(self, tab_index: int):
        """关闭连接

        Args:
            tab_index: 标签页索引
        """
        if tab_index in self._sessions:
            session = self._sessions[tab_index]
            session.disconnect()
            del self._sessions[tab_index]
            self.connection_closed.emit(tab_index)

    def get_session(self, tab_index: int) -> Optional[Session]:
        """获取会话

        Args:
            tab_index: 标签页索引

        Returns:
            Session对象，不存在返回None
        """
        return self._sessions.get(tab_index)

    def get_all_sessions(self) -> List[Session]:
        """获取所有会话"""
        return list(self._sessions.values())

    def close_all_connections(self):
        """关闭所有连接"""
        for session in list(self._sessions.values()):
            session.disconnect()
        self._sessions.clear()

    def _on_connection_closed(self, tab_index: int):
        """连接关闭回调"""
        if tab_index in self._sessions:
            del self._sessions[tab_index]
            self.connection_closed.emit(tab_index)
