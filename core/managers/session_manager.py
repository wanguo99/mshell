"""会话管理器 - 全局会话管理"""

from typing import Dict, List, Optional, Callable
from datetime import datetime
from collections import OrderedDict

from models.session import Session, SessionState


class SessionManager:
    """全局会话管理器

    使用单例模式，管理应用中的所有会话：
    - 活动会话：当前正在运行的会话
    - 历史会话：已断开的会话记录
    - 会话查询：按ID、名称、状态等查询
    - 会话统计：总数、流量、时长等
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # 活动会话：session_id -> Session
        self._active_sessions: OrderedDict[str, Session] = OrderedDict()

        # 历史会话：session_id -> Session（最多保留100条）
        self._history_sessions: OrderedDict[str, Session] = OrderedDict()
        self._max_history = 100

        # 会话事件回调
        self._on_session_created: List[Callable[[Session], None]] = []
        self._on_session_closed: List[Callable[[Session], None]] = []
        self._on_session_state_changed: List[Callable[[Session, SessionState], None]] = []

        self._initialized = True

    # ==================== 会话管理 ====================

    def add_session(self, session: Session) -> bool:
        """添加会话到活动列表

        Args:
            session: 会话对象

        Returns:
            是否添加成功
        """
        if session.session_id in self._active_sessions:
            return False

        self._active_sessions[session.session_id] = session

        # 触发创建事件
        for callback in self._on_session_created:
            try:
                callback(session)
            except Exception as e:
                print(f"会话创建回调错误: {e}")

        return True

    def remove_session(self, session_id: str, save_to_history: bool = True) -> bool:
        """从活动列表移除会话

        Args:
            session_id: 会话ID
            save_to_history: 是否保存到历史记录

        Returns:
            是否移除成功
        """
        if session_id not in self._active_sessions:
            return False

        session = self._active_sessions.pop(session_id)

        # 保存到历史
        if save_to_history:
            self._add_to_history(session)

        # 触发关闭事件
        for callback in self._on_session_closed:
            try:
                callback(session)
            except Exception as e:
                print(f"会话关闭回调错误: {e}")

        return True

    def _add_to_history(self, session: Session):
        """添加会话到历史记录"""
        self._history_sessions[session.session_id] = session

        # 限制历史记录数量
        while len(self._history_sessions) > self._max_history:
            self._history_sessions.popitem(last=False)

    def update_session_state(self, session_id: str, new_state: SessionState):
        """更新会话状态

        Args:
            session_id: 会话ID
            new_state: 新状态
        """
        session = self.get_session(session_id)
        if session:
            old_state = session.state
            session.state = new_state

            # 触发状态变化事件
            for callback in self._on_session_state_changed:
                try:
                    callback(session, old_state)
                except Exception as e:
                    print(f"会话状态变化回调错误: {e}")

    # ==================== 会话查询 ====================

    def get_session(self, session_id: str) -> Optional[Session]:
        """获取活动会话

        Args:
            session_id: 会话ID

        Returns:
            会话对象，不存在返回None
        """
        return self._active_sessions.get(session_id)

    def get_session_by_connection_id(self, connection_id: str) -> Optional[Session]:
        """通过连接配置ID获取会话

        Args:
            connection_id: 连接配置ID

        Returns:
            会话对象，不存在返回None
        """
        for session in self._active_sessions.values():
            if session.connection_id == connection_id:
                return session
        return None

    def get_session_by_name(self, name: str) -> Optional[Session]:
        """通过名称获取会话

        Args:
            name: 会话名称

        Returns:
            会话对象，不存在返回None
        """
        for session in self._active_sessions.values():
            if session.display_name == name:
                return session
        return None

    def get_all_sessions(self) -> List[Session]:
        """获取所有活动会话

        Returns:
            会话列表（按创建时间排序）
        """
        return list(self._active_sessions.values())

    def get_sessions_by_state(self, state: SessionState) -> List[Session]:
        """获取指定状态的会话

        Args:
            state: 会话状态

        Returns:
            会话列表
        """
        return [s for s in self._active_sessions.values() if s.state == state]

    def get_connected_sessions(self) -> List[Session]:
        """获取所有已连接的会话

        Returns:
            已连接会话列表
        """
        return [s for s in self._active_sessions.values() if s.is_connected()]

    def get_history_sessions(self, limit: int = None) -> List[Session]:
        """获取历史会话

        Args:
            limit: 限制数量

        Returns:
            历史会话列表（最新的在前）
        """
        sessions = list(reversed(self._history_sessions.values()))
        if limit:
            return sessions[:limit]
        return sessions

    # ==================== 会话统计 ====================

    def get_session_count(self) -> int:
        """获取活动会话数量"""
        return len(self._active_sessions)

    def get_connected_count(self) -> int:
        """获取已连接会话数量"""
        return len(self.get_connected_sessions())

    def get_total_bytes_sent(self) -> int:
        """获取所有会话发送的总字节数"""
        return sum(s.bytes_sent for s in self._active_sessions.values())

    def get_total_bytes_received(self) -> int:
        """获取所有会话接收的总字节数"""
        return sum(s.bytes_received for s in self._active_sessions.values())

    def get_statistics(self) -> Dict:
        """获取全局统计信息

        Returns:
            统计信息字典
        """
        return {
            'total_sessions': self.get_session_count(),
            'connected_sessions': self.get_connected_count(),
            'total_bytes_sent': self.get_total_bytes_sent(),
            'total_bytes_received': self.get_total_bytes_received(),
            'history_count': len(self._history_sessions)
        }

    # ==================== 事件回调 ====================

    def on_session_created(self, callback: Callable[[Session], None]):
        """注册会话创建回调

        Args:
            callback: 回调函数
        """
        self._on_session_created.append(callback)

    def on_session_closed(self, callback: Callable[[Session], None]):
        """注册会话关闭回调

        Args:
            callback: 回调函数
        """
        self._on_session_closed.append(callback)

    def on_session_state_changed(self, callback: Callable[[Session, SessionState], None]):
        """注册会话状态变化回调

        Args:
            callback: 回调函数
        """
        self._on_session_state_changed.append(callback)

    # ==================== 批量操作 ====================

    def close_all_sessions(self):
        """关闭所有活动会话"""
        for session in list(self._active_sessions.values()):
            session.disconnect()
            self.remove_session(session.session_id)

    def clear_history(self):
        """清空历史记录"""
        self._history_sessions.clear()

    # ==================== 调试信息 ====================

    def __repr__(self):
        return (f"SessionManager(active={self.get_session_count()}, "
                f"connected={self.get_connected_count()}, "
                f"history={len(self._history_sessions)})")


# 全局单例实例
_session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    """获取全局会话管理器实例

    Returns:
        SessionManager单例
    """
    return _session_manager
