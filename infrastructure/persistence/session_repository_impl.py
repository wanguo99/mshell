"""会话仓储实现 - 内存存储"""

from typing import Dict, List, Optional
from domain.session.session_entity import SessionEntity
from domain.session.session_repository import ISessionRepository


class InMemorySessionRepository(ISessionRepository):
    """会话仓储的内存实现

    用于运行时会话管理，不持久化到磁盘。
    """

    def __init__(self):
        self._sessions: Dict[str, SessionEntity] = {}

    def add(self, session: SessionEntity) -> None:
        """添加会话"""
        self._sessions[session.session_id] = session

    def get(self, session_id: str) -> Optional[SessionEntity]:
        """获取会话"""
        return self._sessions.get(session_id)

    def get_all(self) -> List[SessionEntity]:
        """获取所有会话"""
        return list(self._sessions.values())

    def remove(self, session_id: str) -> bool:
        """移除会话"""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def update(self, session: SessionEntity) -> None:
        """更新会话"""
        if session.session_id in self._sessions:
            self._sessions[session.session_id] = session

    def clear(self) -> None:
        """清空所有会话"""
        self._sessions.clear()
