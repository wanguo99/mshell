# MShell 开发指南

本文档为MShell项目的开发指南，适用于三人并行开发模式。

## 📋 目录

1. [项目概览](#项目概览)
2. [开发环境设置](#开发环境设置)
3. [开发人员分工](#开发人员分工)
4. [开发节点与合入策略](#开发节点与合入策略)
5. [开发人员A：平台适配层](#开发人员a平台适配层)
6. [开发人员B：终端核心](#开发人员b终端核心)
7. [开发人员C：UI界面](#开发人员cui界面)
8. [Mock使用指南](#mock使用指南)
9. [集成测试](#集成测试)
10. [代码规范](#代码规范)

---

## 项目概览

**项目名称**: MShell  
**项目目标**: 开发一个跨平台终端工具，支持SSH和串口连接、文件传输、自定义快捷键等功能  
**开发周期**: 8-10天（独立开发5-6天 + 集成测试2-3天 + 缓冲1天）  
**开发模式**: 三人并行开发，基于接口契约和Mock实现解耦

---

## 开发环境设置

### 1. 克隆项目

```bash
git clone <repository-url>
cd mshell
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 创建开发分支

```bash
# 开发人员A
git checkout -b feature/platform-adapter

# 开发人员B
git checkout -b feature/terminal-core

# 开发人员C
git checkout -b feature/ui-filetransfer
```

---

## 开发人员分工

### 👤 开发人员A：平台适配层 + 配置管理
- **负责模块**: `platform/`, `config/`
- **工作量**: 4-5天
- **依赖**: 无，可独立开发
- **特性分支**: `feature/platform-adapter`
- **合入时机**: 第一个合入master（Day 5）

### 👤 开发人员B：终端核心 + 连接管理
- **负责模块**: `terminal/`, `core/`
- **工作量**: 5-6天
- **依赖**: A的platform接口（开发期使用mock）
- **特性分支**: `feature/terminal-core`
- **合入时机**: A合入后，第二个合入master（Day 6）

### 👤 开发人员C：UI界面 + 文件传输
- **负责模块**: `ui/`, `file_transfer/`
- **工作量**: 5-6天
- **依赖**: A和B的接口（开发期使用mock）
- **特性分支**: `feature/ui-filetransfer`
- **合入时机**: B合入后，第三个合入master（Day 7）

---

## 开发节点与合入策略

### 📅 开发时间线

```
Day 1-5:  开发人员A独立开发 platform + config
Day 1-6:  开发人员B独立开发 terminal + core（使用mock）
Day 1-6:  开发人员C独立开发 ui + file_transfer（使用mock）

Day 5:    ✅ 里程碑1 - A完成并合入master
          - B和C切换到master，移除platform mock
          
Day 6:    ✅ 里程碑2 - B完成并合入master
          - C切换到master，移除terminal/core mock
          
Day 7:    ✅ 里程碑3 - C完成并合入master
          - 所有模块集成完成
          
Day 8-9:  集成测试、跨平台测试、bug修复
Day 10:   最终验收、文档完善
```

### 🔄 合入master的条件

每个开发人员在合入master前必须满足以下条件：

#### 开发人员A合入条件（Day 5）
- [ ] 所有`platform/base/`接口基类已实现
- [ ] Windows/Linux/macOS三个平台实现完成
- [ ] `platform/factory.py`工厂类完成
- [ ] `config/config_manager.py`配置管理器完成
- [ ] 单元测试通过（覆盖率 > 80%）
- [ ] 代码审查通过
- [ ] 在至少两个平台上验证功能正常

#### 开发人员B合入条件（Day 6）
- [ ] `terminal/`模块所有文件完成（terminal_widget, ansi_parser, color_scheme）
- [ ] `core/`模块所有文件完成（connection_manager, ssh_connection, serial_connection, command_executor）
- [ ] 已移除platform mock，使用真实platform接口
- [ ] SSH连接测试通过（连接真实服务器）
- [ ] 串口连接测试通过（使用虚拟串口或真实设备）
- [ ] ANSI颜色渲染测试通过
- [ ] 单元测试通过（覆盖率 > 75%）
- [ ] 代码审查通过

#### 开发人员C合入条件（Day 7）
- [ ] `ui/`模块所有文件完成（main_window, connection_dialog, settings_dialog, session_tab）
- [ ] `file_transfer/`模块所有文件完成（sftp_client, file_browser）
- [ ] 已移除所有mock，使用真实接口
- [ ] UI功能测试通过（连接、设置、多标签）
- [ ] 文件传输测试通过（上传、下载、进度显示）
- [ ] 快捷键功能测试通过
- [ ] 单元测试通过（覆盖率 > 70%）
- [ ] 代码审查通过

### 🔀 合入流程

```bash
# 1. 确保本地代码最新
git checkout feature/your-module
git add .
git commit -m "feat: 完成XXX模块开发"

# 2. 切换到master并更新
git checkout master
git pull origin master

# 3. 合并特性分支
git merge feature/your-module

# 4. 解决冲突（如果有）
# 编辑冲突文件...
git add .
git commit -m "merge: 合并feature/your-module到master"

# 5. 运行测试确保没有问题
python -m pytest tests/

# 6. 推送到远程
git push origin master

# 7. 通知其他开发人员更新master
```

### 📢 合入后通知

每次合入master后，负责人需要在团队群中通知：

**开发人员A合入后**:
```
✅ platform + config 模块已合入master
📌 开发人员B和C请执行：
   git checkout master
   git pull origin master
   git checkout feature/your-module
   git merge master
   移除 tests/mock_platform.py 的使用
   改用 from platform.factory import get_platform
```

**开发人员B合入后**:
```
✅ terminal + core 模块已合入master
📌 开发人员C请执行：
   git checkout master
   git pull origin master
   git checkout feature/ui-filetransfer
   git merge master
   移除 tests/mock_terminal.py 和 mock connection 的使用
   改用真实的 TerminalWidget 和 ConnectionManager
```

**开发人员C合入后**:
```
✅ ui + file_transfer 模块已合入master
🎉 所有模块集成完成！
📌 所有人切换到master开始集成测试
```

---

## 开发人员A：平台适配层

### 职责范围

- `platform/base/` - 所有平台接口基类
- `platform/windows/` - Windows平台实现
- `platform/linux/` - Linux平台实现
- `platform/macos/` - macOS平台实现
- `platform/factory.py` - 平台工厂
- `config/config_manager.py` - 配置管理器
- `config/default_config.yaml` - 默认配置

### 开发步骤

#### 第1步：实现base接口（0.5天）

创建以下文件并定义抽象基类：

1. `platform/base/serial.py`
```python
from abc import ABC, abstractmethod
from typing import List

class SerialBase(ABC):
    @abstractmethod
    def get_available_ports(self) -> List[str]:
        """获取可用串口列表"""
        pass
    
    @abstractmethod
    def get_port_description(self, port: str) -> str:
        """获取串口描述信息"""
        pass
```

2. `platform/base/config.py` - 配置路径接口
3. `platform/base/clipboard.py` - 剪贴板接口
4. `platform/base/filesystem.py` - 文件系统接口
5. `platform/base/ui.py` - UI相关接口

#### 第2步：实现Windows平台（1天）

在`platform/windows/`目录下实现所有接口：

```python
# platform/windows/serial.py
from platform.base.serial import SerialBase
import serial.tools.list_ports

class WindowsSerial(SerialBase):
    def get_available_ports(self) -> List[str]:
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def get_port_description(self, port: str) -> str:
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if p.device == port:
                return p.description
        return ""
```

#### 第3步：实现Linux平台（1天）

在`platform/linux/`目录下实现所有接口。

#### 第4步：实现macOS平台（1天）

在`platform/macos/`目录下实现所有接口。

#### 第5步：实现平台工厂（0.5天）

```python
# platform/factory.py
import platform as sys_platform

class Platform:
    def __init__(self):
        self.serial = None
        self.config = None
        self.clipboard = None
        self.filesystem = None
        self.ui = None

def get_platform() -> Platform:
    system = sys_platform.system()
    p = Platform()
    
    if system == "Windows":
        from .windows import serial, config, clipboard, filesystem, ui
        p.serial = serial.WindowsSerial()
        p.config = config.WindowsConfig()
        p.clipboard = clipboard.WindowsClipboard()
        p.filesystem = filesystem.WindowsFilesystem()
        p.ui = ui.WindowsUI()
    elif system == "Linux":
        # Linux实现
        pass
    elif system == "Darwin":
        # macOS实现
        pass
    
    return p
```

#### 第6步：实现配置管理器（0.5天）

```python
# config/config_manager.py
import yaml
from pathlib import Path
from platform.factory import get_platform

class ConfigManager:
    def __init__(self):
        self.platform = get_platform()
        self.config_file = self.platform.config.get_config_dir() / "config.yaml"
        self.config = {}
    
    def load(self):
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
    
    def save(self):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
```

### 测试要点

- 在Windows、Linux、macOS上测试串口枚举
- 验证配置文件路径正确性
- 测试剪贴板操作
- 验证文件管理器打开功能

---

## 开发人员B：终端核心

### 职责范围

- `terminal/terminal_widget.py` - 终端显示组件
- `terminal/ansi_parser.py` - ANSI解析器
- `terminal/color_scheme.py` - 颜色方案
- `core/connection_manager.py` - 连接管理基类
- `core/ssh_connection.py` - SSH连接
- `core/serial_connection.py` - 串口连接
- `core/command_executor.py` - 快捷指令执行器

### 开发步骤

#### 第1步：实现ANSI解析器（1天）

```python
# terminal/ansi_parser.py
import re

class AnsiParser:
    def __init__(self):
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    def parse(self, text: str) -> List[Tuple[str, dict]]:
        """
        解析ANSI转义序列
        返回: [(text, style), ...]
        """
        # 实现ANSI解析逻辑
        pass
```

#### 第2步：实现终端组件（1天）

```python
# terminal/terminal_widget.py
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal

class TerminalWidget(QTextEdit):
    data_to_send = pyqtSignal(bytes)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(False)
        # 使用mock platform（开发阶段）
        from tests.mock_platform import MockPlatform
        self.platform = MockPlatform()
    
    def write_output(self, data: str):
        """显示输出数据"""
        # 使用AnsiParser解析并显示
        pass
    
    def keyPressEvent(self, event):
        # 处理键盘输入
        pass
```

#### 第3步：实现连接管理基类（0.5天）

```python
# core/connection_manager.py
from abc import ABC, abstractmethod
from typing import Callable

class ConnectionManager(ABC):
    def __init__(self):
        self.on_data_received: Callable[[bytes], None] = None
        self.on_connection_changed: Callable[[bool], None] = None
    
    @abstractmethod
    def connect(self, **kwargs) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def send(self, data: bytes):
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        pass
```

#### 第4步：实现SSH连接（1.5天）

```python
# core/ssh_connection.py
import paramiko
import threading
from core.connection_manager import ConnectionManager

class SSHConnection(ConnectionManager):
    def __init__(self):
        super().__init__()
        self.client = None
        self.channel = None
        self._connected = False
    
    def connect(self, host, port, username, password=None, key_file=None):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if password:
                self.client.connect(host, port, username, password)
            elif key_file:
                self.client.connect(host, port, username, key_filename=key_file)
            
            self.channel = self.client.invoke_shell()
            self._connected = True
            
            # 启动接收线程
            threading.Thread(target=self._receive_loop, daemon=True).start()
            
            if self.on_connection_changed:
                self.on_connection_changed(True)
            
            return True
        except Exception as e:
            print(f"SSH连接失败: {e}")
            return False
    
    def _receive_loop(self):
        while self._connected and self.channel:
            if self.channel.recv_ready():
                data = self.channel.recv(1024)
                if self.on_data_received:
                    self.on_data_received(data)
```

#### 第5步：实现串口连接（1天）

使用mock platform获取串口列表。

#### 第6步：实现快捷指令（0.5天）

### 测试要点

- 测试ANSI颜色渲染
- 测试SSH连接到真实服务器
- 测试串口连接（使用虚拟串口）
- 测试终端输入输出

---

## 开发人员C：UI界面

### 职责范围

- `ui/main_window.py` - 主窗口
- `ui/connection_dialog.py` - 连接对话框
- `ui/settings_dialog.py` - 设置对话框
- `ui/session_tab.py` - 会话标签
- `file_transfer/sftp_client.py` - SFTP客户端
- `file_transfer/file_browser.py` - 文件浏览器

### 开发步骤

#### 第1步：实现主窗口（1.5天）

```python
# ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMenuBar, QToolBar
from tests.mock_platform import MockPlatform
from tests.mock_terminal import MockTerminalWidget

class MainWindow(QMainWindow):
    def __init__(self, platform=None):
        super().__init__()
        self.platform = platform or MockPlatform()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("MShell")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        # 添加菜单项...
    
    def add_session_tab(self, name, connection, terminal):
        index = self.tabs.addTab(terminal, name)
        self.tabs.setCurrentIndex(index)
```

#### 第2步：实现连接对话框（1天）

```python
# ui/connection_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QFormLayout

class ConnectionDialog(QDialog):
    def __init__(self, parent, platform):
        super().__init__(parent)
        self.platform = platform
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 连接类型选择
        self.conn_type = QComboBox()
        self.conn_type.addItems(["SSH", "Serial"])
        self.conn_type.currentTextChanged.connect(self.on_type_changed)
        
        # SSH配置表单
        self.ssh_form = self.create_ssh_form()
        
        # Serial配置表单
        self.serial_form = self.create_serial_form()
        
        layout.addWidget(self.conn_type)
        layout.addWidget(self.ssh_form)
        layout.addWidget(self.serial_form)
        
        self.setLayout(layout)
```

#### 第3步：实现设置对话框（1天）

#### 第4步：实现文件传输（2天）

```python
# file_transfer/sftp_client.py
from paramiko import SFTPClient as ParamikoSFTP

class SFTPClient:
    def __init__(self, ssh_connection):
        self.ssh = ssh_connection
        self.sftp = None
    
    def connect(self):
        if self.ssh.client:
            self.sftp = self.ssh.client.open_sftp()
    
    def upload(self, local_path, remote_path, progress_callback=None):
        # 实现上传逻辑
        pass
```

### 测试要点

- 测试UI布局和交互
- 测试对话框功能
- 测试文件传输进度显示
- 测试多标签管理

---

## Mock使用指南

### 创建Mock文件

在`tests/`目录下创建mock实现：

```python
# tests/mock_platform.py
class MockSerial:
    def get_available_ports(self):
        return ["COM1", "COM2", "/dev/ttyUSB0"]

class MockPlatform:
    def __init__(self):
        self.serial = MockSerial()
        # 其他mock...
```

### 使用Mock

在开发阶段，使用mock替代真实依赖：

```python
# 开发阶段
from tests.mock_platform import MockPlatform
platform = MockPlatform()

# 集成阶段（A完成后）
from platform.factory import get_platform
platform = get_platform()
```

---

## 集成测试

### 集成步骤

1. **A完成后**：B和C移除platform相关的mock
2. **B完成后**：C移除terminal和connection相关的mock
3. **全部完成**：进行端到端测试

### 测试清单

- [ ] SSH连接并执行命令
- [ ] 串口连接并收发数据
- [ ] 文件上传下载
- [ ] 快捷键功能
- [ ] 配置保存加载
- [ ] 多标签管理
- [ ] 跨平台测试（Windows/Linux/macOS）

---

## 代码规范

### Python风格

- 遵循PEP 8规范
- 使用类型提示
- 编写docstring

```python
def connect(self, host: str, port: int, username: str) -> bool:
    """
    建立SSH连接
    
    Args:
        host: 主机地址
        port: 端口号
        username: 用户名
    
    Returns:
        bool: 连接是否成功
    """
    pass
```

### 提交规范

```
feat: 添加SSH连接功能
fix: 修复串口断开重连问题
docs: 更新接口文档
test: 添加ANSI解析器测试
refactor: 重构配置管理器
```

### 代码审查

- 提交PR前自我审查
- 确保所有测试通过
- 更新相关文档

---

## 常见问题

### Q: 如何调试跨模块问题？

A: 使用日志记录，在关键位置添加日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"连接参数: {host}:{port}")
```

### Q: Mock何时移除？

A: 当依赖模块完成并通过测试后，逐步移除mock。

### Q: 如何处理接口变更？

A: 在团队群中讨论，更新接口契约文档，通知所有开发人员。

---

## 联系方式

- 技术讨论：[团队群]
- 问题反馈：[Issues]
- 代码审查：[Pull Requests]
