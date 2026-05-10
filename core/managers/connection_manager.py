"""连接管理器，负责管理所有连接会话"""

from typing import Dict, Optional, List
from PyQt5.QtCore import QObject, pyqtSignal

from models.connection import ConnectionConfig, SSHConnectionConfig, SerialConnectionConfig
from models.session import Session
from core.ssh_connection import SSHConnection
from core.serial_connection import SerialConnection
from core.managers.session_manager import get_session_manager
from terminal.terminal_widget import TerminalWidget


class ConnectionManager(QObject):
    """连接管理器

    负责创建和管理连接，会话由全局 SessionManager 管理
    """

    # 信号定义
    connection_created = pyqtSignal(Session)  # 连接创建成功
    connection_closed = pyqtSignal(str)  # 连接关闭（session_id）
    connection_error = pyqtSignal(str)  # 连接错误

    def __init__(self):
        super().__init__()
        self.session_manager = get_session_manager()

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

            # 创建会话
            session = Session(
                config=config,
                connection=ssh_conn,
                terminal=terminal
            )

            # 连接信号
            ssh_conn.data_received.connect(lambda data: self._on_data_received(session, data))
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

            # 设置会话为已连接状态
            session.set_connected()

            # 添加到全局会话管理器
            self.session_manager.add_session(session)

            # 连接状态变化信号
            ssh_conn.connection_changed.connect(lambda connected: self._on_connection_changed(session.session_id, connected))

            self.connection_created.emit(session)
            return session

        except Exception as e:
            self.connection_error.emit(f"创建SSH连接失败: {str(e)}")
            return None

    def _on_data_received(self, session: Session, data: bytes):
        """数据接收回调"""
        session.on_data_received(data)
        session.terminal.write_output(data.decode('utf-8', errors='ignore'))

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

            # 创建会话
            session = Session(
                config=config,
                connection=serial_conn,
                terminal=terminal
            )

            # 连接信号
            serial_conn.data_received.connect(lambda data: self._on_data_received(session, data))
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

            # 设置会话为已连接状态
            session.set_connected()

            # 添加到全局会话管理器
            self.session_manager.add_session(session)

            # 连接状态变化信号
            serial_conn.connection_changed.connect(lambda connected: self._on_connection_changed(session.session_id, connected))

            self.connection_created.emit(session)
            return session

        except Exception as e:
            self.connection_error.emit(f"创建串口连接失败: {str(e)}")
            return None

    def close_connection(self, session_id: str):
        """关闭连接

        Args:
            session_id: 会话ID
        """
        session = self.session_manager.get_session(session_id)
        if session:
            # 断开信号连接
            try:
                session.connection.connection_changed.disconnect()
            except:
                pass

            session.disconnect()
            self.session_manager.remove_session(session_id)

    def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话

        Args:
            session_id: 会话ID

        Returns:
            Session对象，不存在返回None
        """
        return self.session_manager.get_session(session_id)

    def get_session_by_terminal(self, terminal) -> Optional[Session]:
        """通过终端widget获取会话

        Args:
            terminal: 终端widget

        Returns:
            Session对象，不存在返回None
        """
        for session in self.session_manager.get_all_sessions():
            if session.terminal == terminal:
                return session
        return None

    def get_all_sessions(self) -> List[Session]:
        """获取所有会话"""
        return self.session_manager.get_all_sessions()

    def close_all_connections(self):
        """关闭所有连接"""
        for session in self.session_manager.get_all_sessions():
            try:
                session.connection.connection_changed.disconnect()
            except:
                pass
            session.disconnect()
        self.session_manager.close_all_sessions()

    def _on_connection_changed(self, session_id: str, connected: bool):
        """连接状态变化回调"""
        session = self.session_manager.get_session(session_id)
        if not connected and session:
            session.set_disconnected()
            self.connection_closed.emit(session_id)

