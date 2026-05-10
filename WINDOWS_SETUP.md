# Windows 测试指南

## 环境准备

### 1. 安装Python
- 下载Python 3.8+：https://www.python.org/downloads/
- 安装时勾选 "Add Python to PATH"
- 验证安装：
```cmd
python --version
pip --version
```

### 2. 克隆项目
```cmd
git clone https://github.com/wanguo99/mshell.git
cd mshell
```

### 3. 安装依赖
```cmd
pip install -r requirements.txt
```

如果遇到PyQt5安装问题，可以单独安装：
```cmd
pip install PyQt5
pip install paramiko
pip install pyserial
pip install PyYAML
```

## 运行测试

### 1. 运行单元测试
```cmd
# 设置Python路径
set PYTHONPATH=%CD%

# 运行文件传输模块测试
python tests\test_file_transfer.py
```

### 2. 运行主程序（需要其他模块完成后）
```cmd
python main.py
```

## 测试文件传输功能

由于文件传输模块依赖SSH连接，需要先完成以下模块：
- `core/ssh_connection.py` - SSH连接实现
- `terminal/terminal_widget.py` - 终端显示组件
- `ui/main_window.py` - 主窗口

### 临时测试方案（使用Mock）

创建测试脚本 `test_file_browser_demo.py`：

```python
import sys
from PyQt5.QtWidgets import QApplication
from file_transfer.file_browser import FileBrowser
from tests.mock_terminal import MockSSHConnection

# 创建应用
app = QApplication(sys.argv)

# 创建Mock SSH连接
mock_ssh = MockSSHConnection()
mock_ssh.connect(host="test", port=22, username="test", password="test")

# 创建文件浏览器（不传SFTP客户端，只测试本地面板）
browser = FileBrowser()
browser.setWindowTitle("MShell 文件浏览器测试")
browser.resize(900, 600)
browser.show()

sys.exit(app.exec_())
```

运行测试：
```cmd
python test_file_browser_demo.py
```

## 常见问题

### 1. PyQt5安装失败
**问题**：pip安装PyQt5时报错
**解决**：
```cmd
# 使用国内镜像
pip install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者下载wheel文件手动安装
# 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt5
```

### 2. 串口权限问题
**问题**：无法访问COM口
**解决**：以管理员身份运行命令提示符

### 3. 中文乱码
**问题**：终端显示中文乱码
**解决**：
```cmd
# 设置控制台编码为UTF-8
chcp 65001
```

### 4. 找不到模块
**问题**：ModuleNotFoundError
**解决**：
```cmd
# 确保在项目根目录
cd C:\path\to\mshell

# 设置PYTHONPATH
set PYTHONPATH=%CD%
```

## 完整测试流程（等待其他模块完成）

1. **测试平台适配层**
```cmd
python -c "from platform.factory import get_platform; p = get_platform(); print(p.serial.get_available_ports())"
```

2. **测试配置管理**
```cmd
python -c "from config.config_manager import ConfigManager; c = ConfigManager(); c.load(); print(c.get('terminal'))"
```

3. **测试SSH连接**（需要真实SSH服务器）
```cmd
python -c "from core.ssh_connection import SSHConnection; ssh = SSHConnection(); ssh.connect(host='192.168.1.100', port=22, username='root', password='password')"
```

4. **测试文件传输**
```python
from core.ssh_connection import SSHConnection
from file_transfer.sftp_client import SFTPClient

# 连接SSH
ssh = SSHConnection()
ssh.connect(host='192.168.1.100', port=22, username='root', password='password')

# 创建SFTP客户端
sftp = SFTPClient(ssh)

# 列出远程目录
files = sftp.list_dir('/home')
for f in files:
    print(f"{f.name} - {f.size} bytes")

# 上传文件
sftp.upload('local.txt', '/remote/path/file.txt')

# 下载文件
sftp.download('/remote/path/file.txt', 'downloaded.txt')
```

5. **启动完整应用**
```cmd
python main.py
```

## 开发建议

### 使用虚拟环境
```cmd
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 退出虚拟环境
deactivate
```

### IDE配置
推荐使用 **PyCharm** 或 **VS Code**：

**PyCharm**：
1. File → Open → 选择项目目录
2. File → Settings → Project → Python Interpreter
3. 添加虚拟环境或系统Python

**VS Code**：
1. 安装Python扩展
2. Ctrl+Shift+P → Python: Select Interpreter
3. 选择虚拟环境或系统Python

## 下一步

当前文件传输模块已完成，等待以下模块完成后可进行集成测试：
- [ ] core/ssh_connection.py（开发人员B）
- [ ] terminal/terminal_widget.py（开发人员B）
- [ ] ui/main_window.py（开发人员C）

完成后即可在Windows上进行完整的端到端测试。
