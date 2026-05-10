"""新架构集成示例

展示如何在现有 MainWindow 中集成新架构。
"""

import asyncio
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

# 新架构导入
from domain.events.event_bus import EventBus
from domain.events.event_types import SessionCreatedEvent, DataReceivedEvent, SessionClosedEvent
from domain.terminal.engine import TerminalEngine
from application.services.session_orchestrator import SessionOrchestrator
from infrastructure.adapters.async_ssh_adapter import AsyncSSHAdapter
from infrastructure.adapters.async_serial_adapter import AsyncSerialAdapter
from infrastructure.renderers.qt_text_renderer import QtTextRenderer
from infrastructure.async_runtime.async_bridge import AsyncBridge
from infrastructure.persistence.session_repository_impl import InMemorySessionRepository


class NewArchitectureExample(QMainWindow):
    """新架构集成示例

    展示如何使用新架构创建和管理会话。
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MShell - 新架构示例")
        self.resize(800, 600)

        # === 1. 初始化核心组件 ===
        self.event_bus = EventBus()
        self.session_repository = InMemorySessionRepository()
        self.async_bridge = AsyncBridge()

        # === 2. 创建会话编排器 ===
        self.orchestrator = SessionOrchestrator(
            event_bus=self.event_bus,
            session_repository=self.session_repository
        )

        # === 3. 订阅事件 ===
        self.event_bus.subscribe(SessionCreatedEvent, self._on_session_created)
        self.event_bus.subscribe(DataReceivedEvent, self._on_data_received)
        self.event_bus.subscribe(SessionClosedEvent, self._on_session_closed)

        # === 4. 创建 UI ===
        self._init_ui()

        # 会话映射：session_id -> terminal_engine
        self.terminal_engines = {}

    def _init_ui(self):
        """初始化 UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建终端显示组件
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # 创建渲染器和终端引擎
        renderer = QtTextRenderer(self.text_edit, rows=24, cols=80)
        self.terminal_engine = TerminalEngine(renderer, rows=24, cols=80)

    def create_ssh_session(self, host: str, port: int, username: str, password: str):
        """创建 SSH 会话（新架构方式）

        Args:
            host: 主机地址
            port: 端口
            username: 用户名
            password: 密码
        """
        # 使用异步桥接运行协程
        self.async_bridge.run_coroutine(
            self._create_ssh_session_async(host, port, username, password)
        )

    async def _create_ssh_session_async(self, host: str, port: int, username: str, password: str):
        """异步创建 SSH 会话"""
        try:
            # 1. 创建连接适配器
            ssh_adapter = AsyncSSHAdapter()

            # 2. 建立连接
            connected = await ssh_adapter.connect(
                host=host,
                port=port,
                username=username,
                password=password
            )

            if not connected:
                print(f"Failed to connect to {host}")
                return

            # 3. 创建会话
            session = await self.orchestrator.create_session(
                connection=ssh_adapter,
                config={
                    'name': f'{username}@{host}',
                    'host': host,
                    'port': port,
                    'username': username
                }
            )

            if session:
                # 保存终端引擎映射
                self.terminal_engines[session.session_id] = self.terminal_engine
                print(f"Session created: {session.session_id}")

        except Exception as e:
            print(f"Error creating SSH session: {e}")

    def create_serial_session(self, port: str, baudrate: int = 9600):
        """创建串口会话（新架构方式）

        Args:
            port: 串口设备路径
            baudrate: 波特率
        """
        self.async_bridge.run_coroutine(
            self._create_serial_session_async(port, baudrate)
        )

    async def _create_serial_session_async(self, port: str, baudrate: int):
        """异步创建串口会话"""
        try:
            # 1. 创建连接适配器
            serial_adapter = AsyncSerialAdapter()

            # 2. 建立连接
            connected = await serial_adapter.connect(
                port=port,
                baudrate=baudrate
            )

            if not connected:
                print(f"Failed to connect to {port}")
                return

            # 3. 创建会话
            session = await self.orchestrator.create_session(
                connection=serial_adapter,
                config={
                    'name': f'Serial {port}',
                    'port': port,
                    'baudrate': baudrate
                }
            )

            if session:
                self.terminal_engines[session.session_id] = self.terminal_engine
                print(f"Session created: {session.session_id}")

        except Exception as e:
            print(f"Error creating serial session: {e}")

    def send_input(self, session_id: str, data: str):
        """发送输入到会话

        Args:
            session_id: 会话 ID
            data: 要发送的数据
        """
        self.async_bridge.run_coroutine(
            self.orchestrator.send_data(session_id, data.encode('utf-8'))
        )

    # === 事件处理器 ===

    def _on_session_created(self, event: SessionCreatedEvent):
        """会话创建事件处理"""
        print(f"[Event] Session created: {event.session_id} ({event.connection_type})")

    def _on_data_received(self, event: DataReceivedEvent):
        """数据接收事件处理"""
        # 获取对应的终端引擎
        terminal_engine = self.terminal_engines.get(event.session_id)
        if terminal_engine:
            # 写入数据到终端引擎
            terminal_engine.write(event.data.decode('utf-8', errors='ignore'))
            # 渲染（按需渲染，不使用定时器）
            terminal_engine.render()

    def _on_session_closed(self, event: SessionClosedEvent):
        """会话关闭事件处理"""
        print(f"[Event] Session closed: {event.session_id}")
        if event.reason:
            print(f"  Reason: {event.reason}")

        # 清理终端引擎映射
        if event.session_id in self.terminal_engines:
            del self.terminal_engines[event.session_id]

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 关闭所有会话
        self.async_bridge.run_coroutine(self.orchestrator.close_all_sessions())
        # 关闭异步桥接
        self.async_bridge.shutdown()
        event.accept()


# === 使用示例 ===

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # 创建主窗口
    window = NewArchitectureExample()
    window.show()

    # 示例：创建 SSH 会话
    # window.create_ssh_session(
    #     host='example.com',
    #     port=22,
    #     username='user',
    #     password='password'
    # )

    # 示例：创建串口会话
    # window.create_serial_session(
    #     port='/dev/ttyUSB0',
    #     baudrate=115200
    # )

    sys.exit(app.exec_())
