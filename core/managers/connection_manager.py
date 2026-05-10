"""连接管理器，负责管理所有连接会话"""

from typing import Dict, Optional, List
from PyQt5.QtCore import QObject, pyqtSignal

from models.connection import ConnectionConfig, SSHConnectionConfig, SerialConnectionConfig
from models.session import Session
from core.ssh_connection import SSHConnection
from core.serial_connection import SerialConnection
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
            ssh_conn = SSHConnection()

            # 连接信号
            ssh_conn.data_received.connect(lambda data: terminal.write_output(data.decode('utf-8', errors='ignore')))
            terminal.data_to_send.connect(ssh_conn.send)

            # 建立连接
            connect_kwargs = {
                'host': config.host,
                'port': config.port,
                'username': config.username,
            }

            if config.key_file:
                connect_kwargs['key_file'] = config.key_file
            else:
                connect_kwargs['password'] = config.password

            if not ssh_conn.connect(**connect_kwargs):
                self.connection_error.emit(f"SSH连接失败: {config.host}")
                return None

            # 调整终端大小
            ssh_conn.resize_terminal(terminal.cols, terminal.rows)

            # 创建会话
            session = Session(
                tab_index=self._next_tab_index,
                config=config,
                connection=ssh_conn,
                terminal=terminal
            )

            self._sessions[self._next_tab_index] = session

            # 连接状态变化信号
            tab_index = self._next_tab_index
            ssh_conn.connection_changed.connect(lambda connected: self._on_connection_changed(tab_index, connected))

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
            serial_conn = SerialConnection()

            # 连接信号
            serial_conn.data_received.connect(lambda data: terminal.write_output(data.decode('utf-8', errors='ignore')))
            terminal.data_to_send.connect(serial_conn.send)

            # 建立连接
            if not serial_conn.connect(
                port=config.port,
                baudrate=config.baudrate,
                bytesize=config.bytesize,
                parity=config.parity,
                stopbits=config.stopbits
            ):
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

            # 连接状态变化信号
            tab_index = self._next_tab_index
            serial_conn.connection_changed.connect(lambda connected: self._on_connection_changed(tab_index, connected))

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

            # 断开信号连接
            try:
                session.connection.connection_changed.disconnect()
            except:
                pass

            session.disconnect()
            del self._sessions[tab_index]

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
            try:
                session.connection.connection_changed.disconnect()
            except:
                pass
            session.disconnect()
        self._sessions.clear()

    def _on_connection_changed(self, tab_index: int, connected: bool):
        """连接状态变化回调"""
        if not connected and tab_index in self._sessions:
            self.connection_closed.emit(tab_index)

