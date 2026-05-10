# 新架构快速开始指南

## 🚀 快速开始

### 1. 查看新架构代码

新架构代码已经创建在以下目录：

```bash
# 领域层（核心业务逻辑）
domain/
├── events/          # 事件总线
├── connection/      # 连接接口
├── session/         # 会话实体
└── terminal/        # 终端引擎

# 应用层（用例编排）
application/
└── services/        # 会话编排器

# 基础设施层（外部依赖实现）
infrastructure/
├── adapters/        # SSH/串口适配器
├── renderers/       # Qt 渲染器
├── async_runtime/   # 异步桥接
└── persistence/     # 会话仓储
```

### 2. 运行示例代码

```bash
# 查看集成示例
python examples/new_architecture_example.py
```

### 3. 核心概念

#### 3.1 事件驱动

所有模块通过事件总线通信，解耦合：

```python
# 发布事件
event_bus.publish(DataReceivedEvent(session_id='xxx', data=b'hello'))

# 订阅事件
def on_data_received(event: DataReceivedEvent):
    print(f"Received: {event.data}")

event_bus.subscribe(DataReceivedEvent, on_data_received)
```

#### 3.2 异步优先

所有 I/O 操作使用 asyncio：

```python
# 创建连接
ssh_adapter = AsyncSSHAdapter()
await ssh_adapter.connect(host='example.com', username='user', password='pass')

# 发送数据
await ssh_adapter.send(b'ls -la\n')

# 接收数据（异步生成器）
async for data in ssh_adapter.receive():
    print(data)
```

#### 3.3 渲染器抽象

终端引擎与渲染器分离，支持不同渲染后端：

```python
# 创建渲染器
renderer = QtTextRenderer(text_edit, rows=24, cols=80)

# 创建终端引擎
terminal_engine = TerminalEngine(renderer, rows=24, cols=80)

# 写入数据
terminal_engine.write("Hello, World!\n")

# 按需渲染（不使用定时器）
terminal_engine.render()
```

### 4. 性能优化要点

#### 4.1 脏行标记

只重绘变化的行，不重绘整个屏幕：

```python
# TerminalBuffer 自动标记脏行
buffer.feed("new data")

# TerminalEngine 只渲染脏行
terminal_engine.render()  # 仅渲染变化的行
```

#### 4.2 按需渲染

移除定时器，数据到达时才渲染：

```python
# 旧方式（定时器刷新）
self.refresh_timer = QTimer()
self.refresh_timer.timeout.connect(self._render_screen)
self.refresh_timer.start(100)  # 每 100ms 刷新一次

# 新方式（按需渲染）
def on_data_received(event: DataReceivedEvent):
    terminal_engine.write(event.data.decode('utf-8'))
    terminal_engine.render()  # 仅在有数据时渲染
```

#### 4.3 异步 I/O

统一使用 asyncio，避免手动管理线程：

```python
# 旧方式（手动管理线程）
self._receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
self._receive_thread.start()

# 新方式（asyncio）
async def _receive_loop(self, session_id: str):
    async for data in connection.receive():
        event_bus.publish(DataReceivedEvent(session_id, data))
```

### 5. 迁移步骤

#### 步骤 1：创建新的终端视图

```python
# presentation/widgets/terminal_view_v2.py
from PyQt5.QtWidgets import QTextEdit
from domain.terminal.engine import TerminalEngine
from infrastructure.renderers.qt_text_renderer import QtTextRenderer

class TerminalViewV2(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 创建渲染器
        renderer = QtTextRenderer(self, rows=24, cols=80)
        
        # 创建终端引擎
        self.terminal_engine = TerminalEngine(renderer, rows=24, cols=80)
    
    def write_output(self, data: str):
        """写入输出"""
        self.terminal_engine.write(data)
        self.terminal_engine.render()
```

#### 步骤 2：在 MainWindow 中集成

```python
# ui/main_window.py
from domain.events.event_bus import EventBus
from application.services.session_orchestrator import SessionOrchestrator
from infrastructure.async_runtime.async_bridge import AsyncBridge

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 初始化新架构组件
        self.event_bus = EventBus()
        self.async_bridge = AsyncBridge()
        self.orchestrator = SessionOrchestrator(
            event_bus=self.event_bus,
            session_repository=InMemorySessionRepository()
        )
        
        # 订阅事件
        self.event_bus.subscribe(DataReceivedEvent, self._on_data_received)
        
        # ... 其他初始化代码
```

#### 步骤 3：创建会话（新方式）

```python
async def _create_ssh_session_async(self, config):
    # 创建适配器
    adapter = AsyncSSHAdapter()
    
    # 连接
    connected = await adapter.connect(
        host=config.host,
        port=config.port,
        username=config.username,
        password=config.password
    )
    
    if connected:
        # 创建会话
        session = await self.orchestrator.create_session(
            connection=adapter,
            config=config.to_dict()
        )
        return session
```

### 6. 测试新架构

```bash
# 运行单元测试
pytest tests/unit/domain/
pytest tests/unit/infrastructure/
pytest tests/unit/application/

# 运行集成测试
pytest tests/integration/

# 性能测试
python tests/performance/test_terminal_rendering.py
```

### 7. 对比新旧架构

| 特性           | 旧架构                     | 新架构                     |
| -------------- | -------------------------- | -------------------------- |
| 渲染方式       | 定时器刷新（10 FPS）       | 按需渲染（脏行标记）       |
| I/O 模型       | threading 手动管理         | asyncio 统一管理           |
| 模块通信       | PyQt 信号（耦合）          | 事件总线（解耦）           |
| 连接抽象       | 继承混乱                   | 统一 IConnection 接口      |
| 会话管理       | 职责混乱                   | 清晰的编排器模式           |
| 渲染器         | 耦合 QTextEdit             | 可插拔（支持 OpenGL）      |
| 可测试性       | 困难（UI 耦合）            | 容易（依赖注入）           |
| 性能           | CPU 占用高，大量输出卡顿   | CPU 占用低，流畅           |

### 8. 常见问题

#### Q: 新架构会影响现有功能吗？

A: 不会。新旧架构可以并存，逐步迁移。

#### Q: 如何在现有代码中使用新架构？

A: 参考 `examples/new_architecture_example.py`，逐步替换旧组件。

#### Q: 性能提升有多少？

A: 预期 CPU 占用降低 60%+，渲染延迟 < 16ms。

#### Q: 如何调试新架构？

A: 
1. 查看事件总线日志
2. 使用 asyncio 调试工具
3. 单元测试覆盖核心逻辑

### 9. 下一步

1. ✅ 阅读 `docs/ARCHITECTURE_REFACTORING.md`
2. ✅ 运行 `examples/new_architecture_example.py`
3. ⏳ 创建新的 TerminalViewV2
4. ⏳ 在 MainWindow 中集成新架构
5. ⏳ 迁移现有功能
6. ⏳ 性能测试和优化

### 10. 参考资料

- [架构重构方案](./ARCHITECTURE_REFACTORING.md)
- [集成示例](../examples/new_architecture_example.py)
- [领域层代码](../domain/)
- [基础设施层代码](../infrastructure/)

---

**最后更新**：2026-05-10  
**作者**：MShell 架构团队
