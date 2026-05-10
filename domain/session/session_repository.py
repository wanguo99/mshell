"""会话仓储接口"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .session_entity import SessionEntity


class ISessionRepository(ABC):
    """会话仓储接口

    定义会话的持久化操作接口，具体实现由基础设施层提供。
    """

    @abstractmethod
    def add(self, session: SessionEntity) -> None:
        """添加会话"""
        pass

    @abstractmethod
    def get(self, session_id: str) -> Optional[SessionEntity]:
        """获取会话"""
        pass

    @abstractmethod
    def get_all(self) -> List[SessionEntity]:
        """获取所有会话"""
        pass

    @abstractmethod
    def remove(self, session_id: str) -> bool:
        """移除会话"""
        pass

    @abstractmethod
    def update(self, session: SessionEntity) -> None:
        """更新会话"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """清空所有会话"""
        pass
