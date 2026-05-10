# 开发人员B - 工作计划书

## 👤 基本信息

- **负责人**: 开发人员B
- **负责模块**: `terminal/`, `core/`
- **特性分支**: `feature/terminal-core`
- **工作周期**: Day 1 - Day 6（6个工作日）
- **合入时机**: Day 6（第二个合入master）
- **依赖关系**: 依赖开发人员A的platform接口（开发期使用mock）

---

## 🎯 工作目标

实现终端渲染引擎和连接管理模块，支持SSH和串口连接、ANSI颜色渲染、快捷指令执行等核心功能。

---

## 📋 详细任务清单

### Day 1: ANSI解析器实现（8小时）

#### 上午（4小时）
- [ ] **任务1.1**: 创建`terminal/ansi_parser.py`基础框架
  - 定义`AnsiParser`类
  - 实现ANSI转义序列正则表达式
  - 预计时间：1小时

- [ ] **任务1.2**: 实现颜色解析
  - 解析前景色/背景色（30-37, 40-47）
  - 解析256色（38;5;n, 48;5;n）
  - 解析RGB色（38;2;r;g;b, 48;2;r;g;b）
  - 预计时间：2小时

- [ ] **任务1.3**: 实现文本样式解析
  - 粗体、斜体、下划线、闪烁等
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务1.4**: 实现光标控制解析
  - 光标移动（CUU, CUD, CUF, CUB）
  - 光标定位（CUP, HVP）
  - 预计时间：2小时

- [ ] **任务1.5**: 实现清屏和删除操作
  - 清屏（ED）、清行（EL）
  - 预计时间：1小时

- [ ] **任务1.6**: 编写ANSI解析器单元测试
  - 测试各种ANSI序列
  - 预计时间：1小时

---

### Day 2: 终端组件实现（8小时）

#### 上午（4小时）
- [ ] **任务2.1**: 创建`terminal/terminal_widget.py`基础框架
  - 继承`QTextEdit`
  - 定义信号：`data_to_send`
  - 使用mock platform（开发阶段）
  - 预计时间：1小时

- [ ] **任务2.2**: 实现输出显示功能
  - `write_output(data: str)`方法
  - 集成AnsiParser进行颜色渲染
  - 使用QTextCharFormat设置样式
  - 预计时间：2小时

- [ ] **任务2.3**: 实现键盘输入处理
  - 重写`keyPressEvent()`
  - 处理特殊键（Enter, Backspace, Tab, 方向键）
  - 发送`data_to_send`信号
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务2.4**: 实现终端功能
  - `clear()`清屏方法
  - `set_font()`设置字体
  - `set_color_scheme()`设置颜色方案
  - 预计时间：1.5小时

- [ ] **任务2.5**: 实现滚动和历史记录
  - 设置最大行数（scrollback）
  - 自动滚动到底部
  - 预计时间：1小时

- [ ] **任务2.6**: 创建`terminal/color_scheme.py`
  - 定义颜色方案类`ColorScheme`
  - 实现default、solarized_dark、monokai方案
  - 预计时间：1小时

- [ ] **任务2.7**: 终端组件单元测试
  - 测试输入输出
  - 测试颜色渲染
  - 预计时间：0.5小时

---

### Day 3: 连接管理基类 + SSH连接（8小时）

#### 上午（4小时）
- [ ] **任务3.1**: 创建`core/connection_manager.py`
  - 定义`ConnectionManager`抽象基类
  - 定义回调：`on_data_received`, `on_connection_changed`
  - 定义抽象方法：`connect()`, `disconnect()`, `send()`, `is_connected()`
  - 预计时间：1小时

- [ ] **任务3.2**: 创建`core/ssh_connection.py`基础框架
  - 继承`ConnectionManager`
  - 初始化paramiko客户端
  - 预计时间：1小时

- [ ] **任务3.3**: 实现SSH密码认证
  - 实现`connect(host, port, username, password)`
  - 创建SSH客户端和channel
  - 预计时间：1小时

- [ ] **任务3.4**: 实现SSH密钥认证
  - 支持`key_file`参数
  - 处理密钥加载和认证
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务3.5**: 实现SSH数据接收
  - 创建接收线程`_receive_loop()`
  - 调用`on_data_received`回调
  - 预计时间：1.5小时

- [ ] **任务3.6**: 实现SSH数据发送
  - 实现`send(data: bytes)`方法
  - 处理发送异常
  - 预计时间：1小时

- [ ] **任务3.7**: 实现SSH断开连接
  - 实现`disconnect()`方法
  - 清理资源
  - 预计时间：0.5小时

- [ ] **任务3.8**: SSH连接测试
  - 连接真实SSH服务器
  - 测试收发数据
  - 预计时间：1小时

---

### Day 4: 串口连接实现（8小时）

#### 上午（4小时）
- [ ] **任务4.1**: 创建`core/serial_connection.py`基础框架
  - 继承`ConnectionManager`
  - 初始化pyserial
  - 预计时间：1小时

- [ ] **任务4.2**: 实现串口连接
  - 实现`connect(port, baudrate, bytesize, parity, stopbits)`
  - 使用mock platform获取可用串口
  - 预计时间：1.5小时

- [ ] **任务4.3**: 实现串口数据接收
  - 创建接收线程
  - 调用`on_data_received`回调
  - 预计时间：1.5小时

#### 下午（4小时）
- [ ] **任务4.4**: 实现串口数据发送
  - 实现`send(data: bytes)`方法
  - 处理发送异常
  - 预计时间：1小时

- [ ] **任务4.5**: 实现串口断开连接
  - 实现`disconnect()`方法
  - 清理资源
  - 预计时间：0.5小时

- [ ] **任务4.6**: 串口连接测试
  - 使用虚拟串口测试（socat或com0com）
  - 测试收发数据
  - 预计时间：1.5小时

- [ ] **任务4.7**: 编写连接管理单元测试
  - 测试SSH和串口连接
  - 预计时间：1小时

---

### Day 5: 快捷指令 + 移除mock + 测试（8小时）

#### 上午（4小时）
- [ ] **任务5.1**: 创建`core/command_executor.py`
  - 定义`CommandExecutor`类
  - 实现`execute(command: str, connection: ConnectionManager)`
  - 支持变量替换（如{host}, {user}）
  - 预计时间：2小时

- [ ] **任务5.2**: 实现快捷指令管理
  - 从配置加载快捷指令
  - 绑定快捷键
  - 预计时间：1.5小时

- [ ] **任务5.3**: 快捷指令测试
  - 测试指令执行
  - 测试变量替换
  - 预计时间：0.5小时

#### 下午（4小时）
- [ ] **任务5.4**: 移除platform mock
  - 将`from tests.mock_platform import MockPlatform`
  - 改为`from platform.factory import get_platform`
  - 测试与真实platform接口的集成
  - 预计时间：1.5小时

- [ ] **任务5.5**: 完整功能测试
  - SSH连接测试
  - 串口连接测试
  - 终端渲染测试
  - ANSI颜色测试
  - 预计时间：2小时

- [ ] **任务5.6**: 代码审查和优化
  - 检查代码质量
  - 优化性能
  - 添加必要的注释
  - 预计时间：0.5小时

---

### Day 6: 集成测试 + 合入master（8小时）

#### 上午（4小时）
- [ ] **任务6.1**: 端到端测试
  - SSH连接到真实服务器并执行命令
  - 串口连接到真实设备并收发数据
  - 测试ANSI颜色渲染效果
  - 预计时间：2小时

- [ ] **任务6.2**: 跨平台测试
  - 在Windows上测试
  - 在Linux上测试
  - 修复平台特定bug
  - 预计时间：1.5小时

- [ ] **任务6.3**: 性能测试
  - 测试大量数据输出的性能
  - 优化渲染性能
  - 预计时间：0.5小时

#### 下午（4小时）
- [ ] **任务6.4**: 补充单元测试
  - 确保测试覆盖率 > 75%
  - 修复测试失败的用例
  - 预计时间：1.5小时

- [ ] **任务6.5**: 文档完善
  - 更新接口文档
  - 添加使用示例
  - 预计时间：1小时

- [ ] **任务6.6**: 代码最终审查
  - 检查代码规范
  - 移除调试代码
  - 预计时间：0.5小时

- [ ] **任务6.7**: 合入master
  - 提交所有代码
  - 合并到master分支
  - 通知开发人员C
  - 预计时间：1小时

---

## 📦 交付物清单

### 代码文件
- [ ] `terminal/ansi_parser.py`
- [ ] `terminal/terminal_widget.py`
- [ ] `terminal/color_scheme.py`
- [ ] `terminal/__init__.py`
- [ ] `core/connection_manager.py`
- [ ] `core/ssh_connection.py`
- [ ] `core/serial_connection.py`
- [ ] `core/command_executor.py`
- [ ] `core/__init__.py`

### 测试文件
- [ ] `tests/test_ansi_parser.py`
- [ ] `tests/test_terminal_widget.py`
- [ ] `tests/test_ssh_connection.py`
- [ ] `tests/test_serial_connection.py`
- [ ] `tests/test_command_executor.py`

### 文档
- [ ] 接口文档（docstring）
- [ ] 使用示例

---

## ✅ 合入master检查清单

在Day 6合入master前，请确认以下所有项：

- [ ] 所有代码文件已创建并实现
- [ ] 所有单元测试通过（覆盖率 > 75%）
- [ ] SSH连接测试通过（连接真实服务器）
- [ ] 串口连接测试通过（使用虚拟串口或真实设备）
- [ ] ANSI颜色渲染测试通过
- [ ] 已移除platform mock，使用真实接口
- [ ] 在Windows和Linux上测试通过
- [ ] 代码符合PEP 8规范
- [ ] 所有公共接口都有docstring
- [ ] 没有遗留的TODO或FIXME
- [ ] 代码已提交到`feature/terminal-core`分支
- [ ] 已通过自我代码审查

---

## 🔧 开发环境要求

### 必需工具
- Python 3.8+
- Git
- pytest（测试框架）
- SSH服务器（用于测试）
- 虚拟串口工具（socat/com0com）

### 依赖包
```bash
pip install PyQt5
pip install paramiko
pip install pyserial
```

### 测试环境
- SSH服务器：可以使用本地SSH服务或云服务器
- 串口测试：
  - Linux: `socat -d -d pty,raw,echo=0 pty,raw,echo=0`
  - Windows: com0com虚拟串口驱动

---

## 📞 协作要点

### 与开发人员A的协作
- Day 1-4: 使用`tests/mock_platform.py`模拟platform接口
- Day 5: A完成后，切换到真实platform接口
- 如果遇到platform接口问题，及时反馈给A

### 与开发人员C的协作
- C需要使用你的`TerminalWidget`组件显示终端
- C需要使用你的`ConnectionManager`子类管理连接
- 确保接口稳定，避免频繁修改

### 合入后的支持
- Day 6合入后，C会切换到真实接口
- 如果C遇到接口问题，需要及时修复
- Day 7继续提供技术支持

---

## 🚨 风险与应对

### 风险1: ANSI解析复杂度超出预期
- **应对**: 优先实现常用的ANSI序列（颜色、光标移动），复杂的序列可以后续迭代
- **预留时间**: Day 1下午有1小时缓冲

### 风险2: SSH连接稳定性问题
- **应对**: 添加重连机制，处理网络异常
- **实现**: 在`ssh_connection.py`中添加异常处理和重连逻辑

### 风险3: 串口测试环境缺失
- **应对**: 使用虚拟串口工具，或者跳过串口测试（在集成阶段补充）
- **备选方案**: 请团队其他成员帮忙测试真实串口设备

### 风险4: 终端渲染性能问题
- **应对**: 使用批量更新、限制刷新频率
- **实现**: 在`terminal_widget.py`中添加缓冲机制

---

## 📊 进度跟踪

| Day | 计划任务 | 完成状态 | 实际耗时 | 备注 |
|-----|---------|---------|---------|------|
| Day 1 | ANSI解析器 | ⬜ | - | - |
| Day 2 | 终端组件 | ⬜ | - | - |
| Day 3 | 连接管理 + SSH | ⬜ | - | - |
| Day 4 | 串口连接 | ⬜ | - | - |
| Day 5 | 快捷指令 + 移除mock | ⬜ | - | - |
| Day 6 | 集成测试 + 合入 | ⬜ | - | - |

---

## 📝 每日总结模板

### Day X 工作总结
- **完成任务**: 
- **遇到问题**: 
- **解决方案**: 
- **明天计划**: 
- **需要协助**: 

---

## 💡 开发提示

### Mock使用示例
```python
# Day 1-4: 使用mock
from tests.mock_platform import get_mock_platform

class TerminalWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.platform = get_mock_platform()
        font_family, font_size = self.platform.ui.get_default_font()
        self.set_font(font_family, font_size)

# Day 5: 切换到真实接口
from platform.factory import get_platform

class TerminalWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.platform = get_platform()
        font_family, font_size = self.platform.ui.get_default_font()
        self.set_font(font_family, font_size)
```

### SSH连接示例
```python
ssh = SSHConnection()
ssh.on_data_received = lambda data: print(data.decode())
ssh.on_connection_changed = lambda connected: print(f"Connected: {connected}")

if ssh.connect(host="192.168.1.100", port=22, username="root", password="password"):
    ssh.send(b"ls -la\n")
    time.sleep(2)
    ssh.disconnect()
```

---

**祝开发顺利！你的模块是项目的核心引擎，加油！** 🚀
