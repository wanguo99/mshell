# 接口契约文档

本文档定义了三个开发人员之间的接口契约，确保并行开发时模块间的兼容性。

## 开发人员分工

- **开发人员A**：平台适配层 (platform/) + 配置管理 (config/)
- **开发人员B**：终端核心 (terminal/) + 连接管理 (core/)
- **开发人员C**：UI界面 (ui/) + 文件传输 (file_transfer/)

---

## A提供的接口

### 1. Platform接口 (platform/factory.py)

```python
from platform.factory import get_platform

# 获取平台实例
platform = get_platform()

# 串口相关 (B使用)
ports: List[str] = platform.serial.get_available_ports()
description: str = platform.serial.get_port_description(port)

# 配置相关 (C使用)
config_dir: Path = platform.config.get_config_dir()
data_dir: Path = platform.config.get_data_dir()
cache_dir: Path = platform.config.get_cache_dir()

# 剪贴板相关 (B和C使用)
text: str = platform.clipboard.get_text()
platform.clipboard.set_text(text)

# 文件系统相关 (C使用)
normalized_path: str = platform.filesystem.normalize_path(path)
home_dir: Path = platform.filesystem.get_home_dir()
platform.filesystem.open_file_manager(path)
separator: str = platform.filesystem.get_path_separator()

# UI相关 (B和C使用)
font_name, font_size = platform.ui.get_default_font()
fonts: List[str] = platform.ui.get_available_fonts()
modifier: str = platform.ui.get_shortcut_modifier()  # "Ctrl" or "Cmd"
line_ending: str = platform.ui.get_line_ending()  # "\r\n" or "\n"
```

### 2. ConfigManager接口 (config/config_manager.py)

```python
from config.config_manager import ConfigManager

config = ConfigManager()

# 加载配置
config.load()

# 获取配置项
connections = config.get('connections', [])
shortcuts = config.get('shortcuts', {})
terminal_settings = config.get('terminal', {})

# 设置配置项
config.set('connections', connections_list)
config.set('shortcuts', shortcuts_dict)

# 保存配置
config.save()
```

---

## B提供的接口

### 1. TerminalWidget (terminal/terminal_widget.py)

```python
from terminal.terminal_widget import TerminalWidget
from PyQt5.QtCore import pyqtSignal

class TerminalWidget(QWidget):
    # 信号
    data_to_send = pyqtSignal(bytes)  # 用户输入数据
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def write_output(self, data: str):
        """显示输出数据"""
        pass
    
    def clear(self):
        """清空终端"""
        pass
    
    def set_color_scheme(self, scheme_name: str):
        """设置颜色方案"""
        pass
    
    def set_font(self, font_family: str, font_size: int):
        """设置字体"""
        pass
```

### 2. ConnectionManager (core/connection_manager.py)

```python
from core.connection_manager import ConnectionManager
from typing import Callable

class ConnectionManager(ABC):
    def __init__(self):
        self.on_data_received: Callable[[bytes], None] = None
        self.on_connection_changed: Callable[[bool], None] = None
    
    @abstractmethod
    def connect(self, **kwargs) -> bool:
        """建立连接"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    def send(self, data: bytes):
        """发送数据"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """检查连接状态"""
        pass
```

### 3. SSHConnection (core/ssh_connection.py)

```python
from core.ssh_connection import SSHConnection

# 创建SSH连接
ssh = SSHConnection()

# 设置回调
ssh.on_data_received = lambda data: print(data)
ssh.on_connection_changed = lambda connected: print(f"Connected: {connected}")

# 连接
success = ssh.connect(
    host="192.168.1.100",
    port=22,
    username="root",
    password="password",  # 或使用 key_file="/path/to/key"
)

# 发送数据
ssh.send(b"ls -la\n")

# 断开
ssh.disconnect()
```

### 4. SerialConnection (core/serial_connection.py)

```python
from core.serial_connection import SerialConnection

# 创建串口连接
serial = SerialConnection()

# 设置回调
serial.on_data_received = lambda data: print(data)
serial.on_connection_changed = lambda connected: print(f"Connected: {connected}")

# 连接
success = serial.connect(
    port="COM3",  # 或 "/dev/ttyUSB0"
    baudrate=115200,
    bytesize=8,
    parity='N',
    stopbits=1,
)

# 发送数据
serial.send(b"AT\r\n")

# 断开
serial.disconnect()
```

### 5. CommandExecutor (core/command_executor.py)

```python
from core.command_executor import CommandExecutor

executor = CommandExecutor()

# 添加快捷指令
executor.add_command("sys_info", "uname -a")
executor.add_command("disk_usage", "df -h")

# 执行指令（返回替换后的命令）
command = executor.execute("sys_info", context={"host": "server1"})

# 获取所有指令
commands = executor.get_all_commands()
```

---

## C提供的接口

### 1. MainWindow (ui/main_window.py)

```python
from ui.main_window import MainWindow

class MainWindow(QMainWindow):
    def __init__(self, platform):
        super().__init__()
        self.platform = platform
    
    def add_session_tab(self, name: str, connection: ConnectionManager, terminal: TerminalWidget):
        """添加新的会话标签"""
        pass
    
    def remove_session_tab(self, index: int):
        """移除会话标签"""
        pass
    
    def show_message(self, message: str, level: str = "info"):
        """显示消息（info/warning/error）"""
        pass
    
    def update_status(self, message: str):
        """更新状态栏"""
        pass
```

### 2. ConnectionDialog (ui/connection_dialog.py)

```python
from ui.connection_dialog import ConnectionDialog

dialog = ConnectionDialog(parent, platform)

# 显示对话框
if dialog.exec_() == QDialog.Accepted:
    conn_type = dialog.get_connection_type()  # "ssh" or "serial"
    config = dialog.get_connection_config()
    # config 是一个字典，包含连接所需的所有参数
```

### 3. SettingsDialog (ui/settings_dialog.py)

```python
from ui.settings_dialog import SettingsDialog

dialog = SettingsDialog(parent, platform, config_manager)

# 显示对话框
if dialog.exec_() == QDialog.Accepted:
    # 设置已保存到config_manager
    pass
```

### 4. SFTPClient (file_transfer/sftp_client.py)

```python
from file_transfer.sftp_client import SFTPClient

# 从SSH连接创建SFTP客户端
sftp = SFTPClient(ssh_connection)

# 上传文件
sftp.upload(local_path, remote_path, progress_callback=lambda p: print(f"{p}%"))

# 下载文件
sftp.download(remote_path, local_path, progress_callback=lambda p: print(f"{p}%"))

# 列出目录
files = sftp.list_dir(remote_path)

# 删除文件
sftp.remove(remote_path)
```

---

## Mock实现

在集成前，各开发人员可以使用以下mock实现来独立开发：

### B使用的Mock (模拟A的platform)

```python
# tests/mock_platform.py
class MockSerial:
    def get_available_ports(self):
        return ["COM1", "COM2", "/dev/ttyUSB0"]
    
    def get_port_description(self, port):
        return f"Mock Serial Port: {port}"

class MockUI:
    def get_default_font(self):
        return ("Consolas", 12)
    
    def get_line_ending(self):
        return "\n"
    
    def get_shortcut_modifier(self):
        return "Ctrl"

class MockPlatform:
    def __init__(self):
        self.serial = MockSerial()
        self.ui = MockUI()
```

### C使用的Mock (模拟A的platform和B的terminal)

```python
# tests/mock_terminal.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

class MockTerminalWidget(QWidget):
    data_to_send = pyqtSignal(bytes)
    
    def write_output(self, data: str):
        print(f"[Mock Terminal] Output: {data}")
    
    def clear(self):
        print("[Mock Terminal] Cleared")
    
    def set_color_scheme(self, scheme_name: str):
        print(f"[Mock Terminal] Color scheme: {scheme_name}")
    
    def set_font(self, font_family: str, font_size: int):
        print(f"[Mock Terminal] Font: {font_family} {font_size}")

class MockConnectionManager:
    def __init__(self):
        self.on_data_received = None
        self.on_connection_changed = None
        self._connected = False
    
    def connect(self, **kwargs):
        self._connected = True
        if self.on_connection_changed:
            self.on_connection_changed(True)
        return True
    
    def disconnect(self):
        self._connected = False
        if self.on_connection_changed:
            self.on_connection_changed(False)
    
    def send(self, data: bytes):
        print(f"[Mock Connection] Send: {data}")
    
    def is_connected(self):
        return self._connected
```

---

## 数据结构

### 连接配置

```python
# SSH连接配置
ssh_config = {
    "type": "ssh",
    "name": "服务器1",
    "host": "192.168.1.100",
    "port": 22,
    "username": "root",
    "auth_type": "password",  # or "key"
    "password": "secret",  # 如果是password认证
    "key_file": "/path/to/key",  # 如果是key认证
}

# Serial连接配置
serial_config = {
    "type": "serial",
    "name": "串口设备",
    "port": "COM3",
    "baudrate": 115200,
    "bytesize": 8,
    "parity": "N",
    "stopbits": 1,
}
```

### 快捷键配置

```python
shortcuts = {
    "Ctrl+T": "new_tab",
    "Ctrl+W": "close_tab",
    "Ctrl+Shift+C": "copy",
    "Ctrl+Shift+V": "paste",
    "F5": "reconnect",
}
```

### 快捷指令配置

```python
quick_commands = [
    {
        "name": "系统信息",
        "command": "uname -a",
        "shortcut": "F1",
    },
    {
        "name": "磁盘使用",
        "command": "df -h",
        "shortcut": "F2",
    },
]
```

---

## 开发流程

1. **各自开发**：A、B、C按照接口契约独立开发，使用mock模拟依赖
2. **单元测试**：每个模块编写单元测试，确保接口符合契约
3. **集成测试**：移除mock，集成真实模块，进行端到端测试
4. **跨平台测试**：在Windows、Linux、macOS上测试

---

## 注意事项

1. **接口稳定性**：一旦接口定义，不要随意修改，如需修改需通知其他开发人员
2. **类型提示**：使用Python类型提示，便于IDE自动补全和类型检查
3. **异常处理**：所有接口都应该有明确的异常处理和错误返回
4. **文档字符串**：每个公共接口都应该有docstring说明用途和参数
5. **线程安全**：涉及多线程的接口（如连接管理）需要考虑线程安全
