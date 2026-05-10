"""会话编排器 - 协调会话的创建、管理和销毁

职责：
- 创建和管理会话生命周期
- 协调连接适配器和终端引擎
- 发布会话相关事件
- 处理数据接收循环
"""

import asyncio
import uuid
from typing import Dict, Optional
from domain.connection.connection import IConnection
from domain.session.session_entity import SessionEntity, SessionState
from domain.session.session_repository import ISessionRepository
from domain.events.event_bus import EventBus
from domain.events.event_types import (
    SessionCreatedEvent,
    SessionClosedEvent,
    DataReceivedEvent,
    ConnectionStateChangedEvent
)


class SessionOrchestrator:
    """会话编排器

    协调会话的创建、数据流转和销毁。
    """

    def __init__(self, event_bus: EventBus, session_repository: ISessionRepository):
        """初始化会话编排器

        Args:
            event_bus: 事件总线
            session_repository: 会话仓储
        """
        self.event_bus = event_bus
        self.session_repository = session_repository
        self._connections: Dict[str, IConnection] = {}  # session_id -> connection
        self._receive_tasks: Dict[str, asyncio.Task] = {}  # session_id -> receive_task

    async def create_session(self, connection: IConnection, config: dict) -> Optional[SessionEntity]:
        """创建会话

        Args:
            connection: 连接适配器（已连接）
            config: 连接配置

        Returns:
            会话实体，失败返回 None
        """
        try:
            # 生成会话 ID
            session_id = str(uuid.uuid4())

            # 创建会话实体
            session = SessionEntity(
                session_id=session_id,
                connection_type=connection.connection_type,
                name=config.get('name', f'{connection.connection_type}_{session_id[:8]}'),
                config=config
            )

            # 设置为已连接状态
            session.set_connected()

            # 保存到仓储
            self.session_repository.add(session)

            # 保存连接引用
            self._connections[session_id] = connection

            # 启动数据接收循环
            receive_task = asyncio.create_task(self._receive_loop(session_id))
            self._receive_tasks[session_id] = receive_task

            # 发布会话创建事件
            self.event_bus.publish(SessionCreatedEvent(
                session_id=session_id,
                connection_type=connection.connection_type,
                name=session.name
            ))

            return session

        except Exception as e:
            print(f"Failed to create session: {e}")
            return None

    async def close_session(self, session_id: str, reason: Optional[str] = None) -> None:
        """关闭会话

        Args:
            session_id: 会话 ID
            reason: 关闭原因
        """
        # 获取会话
        session = self.session_repository.get(session_id)
        if not session:
            return

        # 取消接收任务
        if session_id in self._receive_tasks:
            task = self._receive_tasks[session_id]
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self._receive_tasks[session_id]

        # 断开连接
        if session_id in self._connections:
            connection = self._connections[session_id]
            await connection.disconnect()
            del self._connections[session_id]

        # 更新会话状态
        session.set_disconnected(reason)
        self.session_repository.update(session)

        # 发布会话关闭事件
        self.event_bus.publish(SessionClosedEvent(
            session_id=session_id,
            reason=reason
        ))

        # 从仓储中移除
        self.session_repository.remove(session_id)

    async def send_data(self, session_id: str, data: bytes) -> None:
        """发送数据到会话

        Args:
            session_id: 会话 ID
            data: 要发送的数据
        """
        connection = self._connections.get(session_id)
        if not connection or not connection.is_connected():
            return

        try:
            await connection.send(data)

            # 更新会话统计
            session = self.session_repository.get(session_id)
            if session:
                session.record_sent(len(data))
                self.session_repository.update(session)

        except Exception as e:
            print(f"Failed to send data: {e}")
            await self.close_session(session_id, f"Send error: {e}")

    async def resize_terminal(self, session_id: str, rows: int, cols: int) -> None:
        """调整终端大小

        Args:
            session_id: 会话 ID
            rows: 行数
            cols: 列数
        """
        connection = self._connections.get(session_id)
        if connection:
            await connection.resize_terminal(rows, cols)

    def get_session(self, session_id: str) -> Optional[SessionEntity]:
        """获取会话

        Args:
            session_id: 会话 ID

        Returns:
            会话实体
        """
        return self.session_repository.get(session_id)

    async def close_all_sessions(self) -> None:
        """关闭所有会话"""
        session_ids = [s.session_id for s in self.session_repository.get_all()]
        for session_id in session_ids:
            await self.close_session(session_id)

    async def _receive_loop(self, session_id: str) -> None:
        """数据接收循环

        Args:
            session_id: 会话 ID
        """
        connection = self._connections.get(session_id)
        if not connection:
            return

        try:
            async for data in connection.receive():
                # 调试：检查 data 类型
                if not isinstance(data, bytes):
                    print(f"WARNING: Received non-bytes data: {type(data)} = {data}")
                    continue

                # 更新会话统计
                session = self.session_repository.get(session_id)
                if session:
                    data_len = len(data)
                    session.record_received(data_len)
                    self.session_repository.update(session)

                # 发布数据接收事件
                event = DataReceivedEvent(
                    session_id=session_id,
                    data=data
                )
                self.event_bus.publish(event)

        except asyncio.CancelledError:
            # 正常取消
            pass
        except Exception as e:
            print(f"Receive loop error: {e}")
            await self.close_session(session_id, f"Receive error: {e}")
