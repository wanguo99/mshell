"""事件总线 - 轻量级发布订阅实现"""

from typing import Dict, List, Callable, Type, Any
from dataclasses import dataclass
import asyncio
from collections import defaultdict


@dataclass
class Event:
    """事件基类"""
    pass


class EventBus:
    """事件总线（支持同步和异步订阅）

    用于模块间解耦通信，避免直接依赖。
    """

    def __init__(self):
        # 同步订阅者
        self._subscribers: Dict[Type[Event], List[Callable]] = defaultdict(list)
        # 异步订阅者
        self._async_subscribers: Dict[Type[Event], List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: Type[Event], handler: Callable) -> None:
        """订阅事件（同步处理器）

        Args:
            event_type: 事件类型
            handler: 事件处理函数 (event: Event) -> None
        """
        self._subscribers[event_type].append(handler)

    def subscribe_async(self, event_type: Type[Event], handler: Callable) -> None:
        """订阅事件（异步处理器）

        Args:
            event_type: 事件类型
            handler: 异步事件处理函数 async (event: Event) -> None
        """
        self._async_subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: Type[Event], handler: Callable) -> None:
        """取消订阅

        Args:
            event_type: 事件类型
            handler: 要移除的处理函数
        """
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
        if handler in self._async_subscribers[event_type]:
            self._async_subscribers[event_type].remove(handler)

    def publish(self, event: Event) -> None:
        """发布事件（同步）

        Args:
            event: 事件实例
        """
        event_type = type(event)

        # 调试：检查事件类型
        if not isinstance(event, Event):
            print(f"ERROR: publish() received non-Event object: {type(event)} = {event}")
            return

        # 调用同步订阅者
        for handler in self._subscribers[event_type]:
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler {handler.__name__}: {e}")
                print(f"  Event type: {type(event)}")
                print(f"  Event value: {event}")

        # 调度异步订阅者
        for handler in self._async_subscribers[event_type]:
            try:
                asyncio.create_task(handler(event))
            except Exception as e:
                print(f"Error scheduling async handler {handler.__name__}: {e}")

    async def publish_async(self, event: Event) -> None:
        """发布事件（异步，等待所有处理器完成）

        Args:
            event: 事件实例
        """
        event_type = type(event)

        # 调用同步订阅者
        for handler in self._subscribers[event_type]:
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler {handler.__name__}: {e}")

        # 等待所有异步订阅者完成
        tasks = []
        for handler in self._async_subscribers[event_type]:
            try:
                tasks.append(asyncio.create_task(handler(event)))
            except Exception as e:
                print(f"Error scheduling async handler {handler.__name__}: {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def clear(self) -> None:
        """清空所有订阅"""
        self._subscribers.clear()
        self._async_subscribers.clear()
