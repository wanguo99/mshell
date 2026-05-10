"""asyncio 与 Qt 事件循环的桥接

解决 asyncio 与 PyQt 事件循环集成的问题。
"""

import asyncio
from typing import Coroutine, Optional
from PyQt5.QtCore import QObject, QTimer


class AsyncBridge(QObject):
    """asyncio 与 Qt 事件循环的桥接器

    使用 QTimer 驱动 asyncio 事件循环，避免阻塞 Qt 主线程。
    """

    def __init__(self, interval: int = 10):
        """初始化异步桥接器

        Args:
            interval: 事件循环处理间隔（毫秒），默认 10ms
        """
        super().__init__()

        # 创建 asyncio 事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # 使用 QTimer 驱动 asyncio 事件循环
        self.timer = QTimer()
        self.timer.timeout.connect(self._process_events)
        self.timer.start(interval)

        self._running = True

    def _process_events(self):
        """处理 asyncio 事件

        在 Qt 事件循环的每个周期中处理 asyncio 事件。
        """
        if not self._running:
            return

        # 运行所有就绪的协程
        self.loop.stop()
        self.loop.run_forever()

    def run_coroutine(self, coro: Coroutine) -> asyncio.Task:
        """在 asyncio 循环中运行协程

        Args:
            coro: 协程对象

        Returns:
            asyncio.Task 对象
        """
        return asyncio.ensure_future(coro, loop=self.loop)

    def run_coroutine_sync(self, coro: Coroutine):
        """同步运行协程（阻塞直到完成）

        Args:
            coro: 协程对象

        Returns:
            协程的返回值
        """
        return self.loop.run_until_complete(coro)

    def shutdown(self):
        """关闭事件循环"""
        self._running = False
        self.timer.stop()

        # 获取所有待处理的任务
        pending = asyncio.all_tasks(self.loop)

        if pending:
            # 取消所有待处理的任务
            for task in pending:
                task.cancel()

            # 运行事件循环直到所有任务被取消
            try:
                self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception as e:
                print(f"Error during shutdown: {e}")

        # 关闭事件循环
        self.loop.close()
