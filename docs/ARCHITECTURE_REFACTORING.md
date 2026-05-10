# MShell 架构重构方案

## 📋 目录

- [1. 当前架构诊断](#1-当前架构诊断)
- [2. 目标架构设计](#2-目标架构设计)
- [3. 新架构目录结构](#3-新架构目录结构)
- [4. 关键组件设计](#4-关键组件设计)
- [5. 重构路线图](#5-重构路线图)
- [6. 性能优化要点](#6-性能优化要点)

---

## 1. 当前架构诊断

### 主要问题

#### 🔴 严重问题

1. **终端渲染与业务逻辑耦合**
   - `TerminalWidget` 同时承担 VT100 解析、Qt 渲染、键盘处理、颜色管理
   - 每次刷新都重绘整个屏幕区域，性能瓶颈明显
   - 渲染逻辑直接操作 QTextEdit，无法切换渲染后端

2. **连接层设计混乱**
   - `SSHConnection` 继承自 `ConnectionManager`（命名错误）
   - 线程管理分散，无统一调度
   - 信号机制与 threading 混用，存在线程安全隐患

3. **会话管理职责不清**
   - `Session` 既是数据模型又包含业务逻辑
   - `ConnectionManager` 和 `SessionManager` 职责重叠
   - UI 层直接持有 `terminal_to_session` 映射

4. **缺乏事件总线**
   - 使用 PyQt 信号机制，跨模块通信困难
   - 无法实现插件系统的事件订阅

5. **性能优化不足**
   - 10 FPS 定时器刷新率仍然过高
   - 大量输出时（如 `cat large_file`）会卡顿
   - 历史缓冲区管理效率低

### 架构评分

| 维度       | 当前评分 | 目标评分 | 说明                                   |
| ---------- | -------- | -------- | -------------------------------------- |
| 可维护性   | 6/10     | 9/10     | 分层清晰但职责混乱                     |
| 可扩展性   | 5/10     | 9/10     | 新增协议需要修改多个管理器             |
| 可测试性   | 4/10     | 8/10     | UI 与业务逻辑耦合严重                  |
| 性能       | 5/10     | 9/10     | 存在明显瓶颈，大量输出时渲染卡顿       |

---

## 2. 目标架构设计

### 整体架构：分层架构 + 事件驱动 + 插件化

采用 **Clean Architecture** 的变体，结合终端应用的特点：

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer (UI)                   │
│  PyQt5 Widgets, Dialogs, Theme, Keyboard Handlers           │
└─────────────────────────────────────────────────────────────┘
                              ↕ (Events)
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer (App)                    │
│  Session Orchestrator, Tab Manager, Use Cases               │
└─────────────────────────────────────────────────────────────┘
                              ↕ (Interfaces)
┌─────────────────────────────────────────────────────────────┐
│                    Domain Layer (Core)                       │
│  Session Entity, Connection Interface, Terminal Engine      │
│  Event Bus (核心通信机制)                                    │
└─────────────────────────────────────────────────────────────┘
                              ↕ (Implementations)
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer (Infra)                 │
│  SSH/Serial Adapters, Qt Renderer, Config Storage           │
└─────────────────────────────────────────────────────────────┘
```

### 核心设计原则

1. **依赖倒置**：高层模块不依赖低层模块，都依赖抽象
2. **协议与渲染分离**：终端引擎只负责状态管理，渲染器可插拔
3. **异步优先**：使用 `asyncio` 统一管理 I/O
4. **事件驱动**：模块间通过事件总线通信，解耦合
5. **接口抽象**：所有外部依赖通过接口注入

---

## 3. 新架构目录结构

```
mshell/
├── domain/                  # 领域层（核心业务逻辑，无外部依赖）⭐
│   ├── events/              # 事件系统
│   │   ├── event_bus.py     # 事件总线实现
│   │   └── event_types.py   # 事件类型定义
│   ├── connection/          # 连接抽象
│   │   └── connection.py    # IConnection 接口
│   ├── session/             # 会话领域
│   │   ├── session_entity.py       # 会话实体（纯数据）
│   │   └── session_repository.py   # 会话仓储接口
│   └── terminal/            # 终端引擎
│       ├── buffer.py        # 终端缓冲区（脏行标记）
│       └── engine.py        # 终端引擎（协调器）
│
├── application/             # 应用层（用例编排）
│   └── services/
│       └── session_orchestrator.py  # 会话编排器
│
├── infrastructure/          # 基础设施层（外部依赖实现）
│   ├── adapters/            # 连接适配器
│   │   ├── async_ssh_adapter.py     # SSH 适配器
│   │   └── async_serial_adapter.py  # 串口适配器
│   ├── renderers/           # 渲染器实现
│   │   └── qt_text_renderer.py      # Qt 渲染器
│   ├── async_runtime/       # 异步运行时
│   │   └── async_bridge.py          # asyncio <-> Qt 桥接
│   └── persistence/         # 持久化
│       └── session_repository_impl.py
│
├── presentation/            # 表现层（UI）
│   ├── main_window.py
│   └── widgets/
│       └── terminal_view.py # 终端视图（薄包装）
│
└── plugins/                 # 插件系统（未来扩展）
    └── plugin_manager.py
```

---

## 4. 关键组件设计

### 4.1 事件总线（Event Bus）

**位置**：`domain/events/event_bus.py`

**职责**：
- 提供发布-订阅机制
- 支持同步和异步事件处理
- 解耦模块间通信

**核心事件**：
```python
@dataclass
class SessionCreatedEvent(Event):
    session_id: str
    connection_type: str
    name: str

@dataclass
class DataReceivedEvent(Event):
    session_id: str
    data: bytes

@dataclass
class SessionClosedEvent(Event):
    session_id: str
    reason: Optional[str] = None
```

### 4.2 连接接口（IConnection）

**位置**：`domain/connection/connection.py`

**职责**：
- 定义所有连接类型的统一接口
- 使用异步接口（asyncio）

**接口定义**：
```python
class IConnection(ABC):
    @abstractmethod
    async def connect(self, **kwargs) -> bool: ...
    
    @abstractmethod
    async def disconnect(self) -> None: ...
    
    @abstractmethod
    async def send(self, data: bytes) -> None: ...
    
    @abstractmethod
    async def receive(self) -> AsyncIterator[bytes]: ...
    
    @abstractmethod
    def is_connected(self) -> bool: ...
```

### 4.3 终端引擎（Terminal Engine）

**位置**：`domain/terminal/engine.py`

**架构**：Parser (pyte) → Buffer (脏行标记) → Renderer (可插拔)

**核心优化**：
1. **脏行标记**：只重绘变化的行
2. **按需渲染**：数据到达时才渲染，不使用定时器
3. **渲染器抽象**：支持不同渲染后端（Qt、OpenGL）

**数据流**：
```
数据输入 → TerminalBuffer.feed()
         → 标记脏行
         → TerminalEngine.render()
         → 仅渲染脏行
         → Renderer.render_line()
```

### 4.4 会话编排器（Session Orchestrator）

**位置**：`application/services/session_orchestrator.py`

**职责**：
- 创建和管理会话生命周期
- 协调连接适配器和终端引擎
- 发布会话相关事件
- 处理数据接收循环

**核心方法**：
```python
class SessionOrchestrator:
    async def create_session(self, connection: IConnection, config: dict) -> SessionEntity
    async def close_session(self, session_id: str, reason: Optional[str] = None)
    async def send_data(self, session_id: str, data: bytes)
    async def _receive_loop(self, session_id: str)  # 数据接收循环
```

### 4.5 异步桥接（Async Bridge）

**位置**：`infrastructure/async_runtime/async_bridge.py`

**职责**：
- 集成 asyncio 与 PyQt 事件循环
- 使用 QTimer 驱动 asyncio 事件循环

**实现原理**：
```python
class AsyncBridge(QObject):
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.timer = QTimer()
        self.timer.timeout.connect(self._process_events)
        self.timer.start(10)  # 每 10ms 处理一次
    
    def _process_events(self):
        self.loop.stop()
        self.loop.run_forever()
```

---

## 5. 重构路线图

### 阶段 1：领域层核心模块（已完成 ✅）

**目标**：建立核心领域模型和接口

**完成内容**：
- ✅ 事件总线（`domain/events/`）
- ✅ 连接接口（`domain/connection/`）
- ✅ 会话实体（`domain/session/`）
- ✅ 终端引擎（`domain/terminal/`）

**风险控制**：
- 领域层无外部依赖，可独立测试
- 不影响现有代码运行

### 阶段 2：基础设施层适配器（已完成 ✅）

**目标**：实现异步连接适配器和渲染器

**完成内容**：
- ✅ 异步 SSH 适配器（`infrastructure/adapters/async_ssh_adapter.py`）
- ✅ 异步串口适配器（`infrastructure/adapters/async_serial_adapter.py`）
- ✅ Qt 渲染器（`infrastructure/renderers/qt_text_renderer.py`）
- ✅ 异步桥接（`infrastructure/async_runtime/async_bridge.py`）
- ✅ 会话仓储实现（`infrastructure/persistence/`）

**风险控制**：
- 适配器实现 IConnection 接口，可单独测试
- 渲染器实现 IRenderer 接口，可替换

### 阶段 3：应用层编排器（已完成 ✅）

**目标**：实现会话编排和用例

**完成内容**：
- ✅ 会话编排器（`application/services/session_orchestrator.py`）
- ⏳ 标签页管理器（待实现）
- ⏳ 用例层（待实现）

**风险控制**：
- 应用层依赖领域层接口，可 mock 测试
- 逐步替换旧的 ConnectionManager

### 阶段 4：UI 层集成（进行中 🔄）

**目标**：集成新架构到现有 UI

**任务**：
- ⏳ 创建新的 TerminalView（使用 TerminalEngine）
- ⏳ 重构 MainWindow（使用 SessionOrchestrator）
- ⏳ 订阅事件总线事件
- ⏳ 迁移现有功能

**风险控制**：
- 保留旧代码作为备份
- 逐个标签页迁移，支持新旧并存
- 充分测试后再删除旧代码

### 阶段 5：性能优化与测试（待开始 ⏳）

**目标**：优化性能并完善测试

**任务**：
- 性能测试（大量输出场景）
- 内存泄漏检测
- 单元测试覆盖率 > 80%
- 集成测试

**风险控制**：
- 性能基准测试
- 压力测试
- 回归测试

### 阶段 6：插件系统与高级特性（未来 🔮）

**目标**：实现插件系统和高级功能

**任务**：
- 插件管理器
- 触发器插件
- 宏插件
- 脚本引擎集成

---

## 6. 性能优化要点

### 6.1 终端渲染优化

**当前问题**：
- 10 FPS 定时器刷新，即使无数据也刷新
- 每次刷新重绘整个屏幕区域
- 历史缓冲区逐行删除效率低

**优化方案**：
1. **脏行标记**：只重绘变化的行
2. **按需渲染**：数据到达时才渲染，移除定时器
3. **双缓冲**：避免渲染撕裂
4. **批量处理**：累积数据后一次性渲染

**预期效果**：
- CPU 占用降低 60%+
- 大量输出时不卡顿
- 渲染延迟 < 16ms

### 6.2 异步 I/O 优化

**当前问题**：
- 使用 threading 手动管理线程
- 信号机制与线程混用，线程安全隐患

**优化方案**：
1. 统一使用 asyncio 管理 I/O
2. 通过 AsyncBridge 集成 Qt 事件循环
3. 使用 `asyncio.to_thread` 包装同步操作

**预期效果**：
- 代码更简洁，易维护
- 无线程安全问题
- 支持高并发连接

### 6.3 内存优化

**当前问题**：
- 历史缓冲区无限增长
- 会话对象未及时释放

**优化方案**：
1. 限制历史缓冲区大小
2. 会话关闭时及时清理资源
3. 使用弱引用避免循环引用

---

## 7. 迁移指南

### 7.1 如何使用新架构创建会话

```python
# 1. 初始化依赖
event_bus = EventBus()
session_repository = InMemorySessionRepository()
async_bridge = AsyncBridge()

# 2. 创建会话编排器
orchestrator = SessionOrchestrator(event_bus, session_repository)

# 3. 创建连接适配器
ssh_adapter = AsyncSSHAdapter()
connected = await ssh_adapter.connect(
    host='example.com',
    port=22,
    username='user',
    password='pass'
)

# 4. 创建会话
if connected:
    session = await orchestrator.create_session(
        connection=ssh_adapter,
        config={'name': 'My SSH Session', 'host': 'example.com'}
    )

# 5. 订阅数据接收事件
def on_data_received(event: DataReceivedEvent):
    terminal_engine.write(event.data.decode('utf-8', errors='ignore'))
    terminal_engine.render()

event_bus.subscribe(DataReceivedEvent, on_data_received)

# 6. 发送数据
await orchestrator.send_data(session.session_id, b'ls -la\n')
```

### 7.2 如何使用新的终端引擎

```python
# 1. 创建渲染器
text_edit = QTextEdit()
renderer = QtTextRenderer(text_edit, rows=24, cols=80)

# 2. 创建终端引擎
terminal_engine = TerminalEngine(renderer, rows=24, cols=80)

# 3. 写入数据
terminal_engine.write("Hello, World!\n")

# 4. 渲染（按需调用，不使用定时器）
terminal_engine.render()
```

---

## 8. 测试策略

### 8.1 单元测试

**领域层**：
- 事件总线：发布订阅机制
- 终端缓冲区：脏行标记逻辑
- 会话实体：状态转换

**基础设施层**：
- 连接适配器：连接、断开、发送、接收
- 渲染器：行渲染、光标渲染

### 8.2 集成测试

- 会话编排器 + 连接适配器
- 终端引擎 + 渲染器
- 事件总线 + 应用层

### 8.3 性能测试

- 大量输出场景（10MB 数据）
- 多会话并发（10+ 会话）
- 内存泄漏检测

---

## 9. 常见问题

### Q1: 为什么要重构？

**A**: 当前架构存在严重的耦合问题，导致：
- 难以添加新协议（需要修改多处）
- 性能瓶颈难以优化（渲染逻辑耦合）
- 无法实现插件系统（缺乏事件机制）
- 测试困难（UI 与业务逻辑耦合）

### Q2: 重构会影响现有功能吗？

**A**: 不会。重构采用渐进式策略：
- 新旧代码并存
- 逐步迁移功能
- 充分测试后再删除旧代码

### Q3: 性能会提升多少？

**A**: 预期提升：
- CPU 占用降低 60%+
- 渲染延迟 < 16ms
- 支持 10+ 并发会话无卡顿

### Q4: 如何参与重构？

**A**: 
1. 阅读本文档
2. 查看 `domain/`、`application/`、`infrastructure/` 目录
3. 运行单元测试：`pytest tests/unit/`
4. 提交 PR

---

## 10. 参考资料

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [asyncio 文档](https://docs.python.org/3/library/asyncio.html)
- [PyQt5 文档](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

---

**最后更新**：2026-05-10  
**作者**：MShell 架构团队
