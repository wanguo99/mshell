# 开发人员C - 工作计划书

## 👤 基本信息

- **负责人**: 开发人员C
- **负责模块**: `ui/`, `file_transfer/`
- **特性分支**: `feature/ui-filetransfer`
- **工作周期**: Day 1 - Day 7（7个工作日）
- **合入时机**: Day 7（第三个合入master）
- **依赖关系**: 依赖开发人员A的platform接口和开发人员B的terminal/core接口（开发期使用mock）

---

## 🎯 工作目标

实现用户界面和文件传输模块，提供完整的图形界面、连接管理、设置配置、多标签会话和SFTP文件传输功能。

---

## 📋 详细任务清单

### Day 1: 主窗口框架实现（8小时）

#### 上午（4小时）
- [ ] **任务1.1**: 创建`ui/main_window.py`基础框架
  - 继承`QMainWindow`
  - 使用mock platform和terminal
  - 预计时间：1小时

- [ ] **任务1.2**: 实现菜单栏
  - 文件菜单：新建连接、退出
  - 编辑菜单：复制、粘贴、清屏
  - 视图菜单：字体设置、颜色方案
  - 帮助菜单：关于
  - 预计时间：2小时

- [ ] **任务1.3**: 实现工具栏
  - 新建连接按钮
  - 断开连接按钮
  - 设置按钮
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务1.4**: 实现标签页管理
  - 创建`QTabWidget`
  - 实现`add_session_tab()`方法
  - 实现`close_session_tab()`方法
  - 标签页右键菜单（关闭、关闭其他、关闭所有）
  - 预计时间：2小时

- [ ] **任务1.5**: 实现状态栏
  - 显示连接状态
  - 显示当前会话信息
  - 预计时间：1小时

- [ ] **任务1.6**: 主窗口布局和样式
  - 设置窗口大小和位置
  - 应用样式表
  - 预计时间：1小时

---

### Day 2: 会话标签和连接对话框（8小时）

#### 上午（4小时）
- [ ] **任务2.1**: 创建`ui/session_tab.py`
  - 定义`SessionTab`类
  - 包含终端组件（使用mock）
  - 包含连接对象
  - 预计时间：1.5小时

- [ ] **任务2.2**: 实现会话标签功能
  - 连接终端和连接管理器
  - 处理数据收发
  - 实现连接状态更新
  - 预计时间：1.5小时

- [ ] **任务2.3**: 实现会话标签右键菜单
  - 复制、粘贴
  - 清屏
  - 断开连接
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务2.4**: 创建`ui/connection_dialog.py`基础框架
  - 继承`QDialog`
  - 连接类型选择（SSH/Serial）
  - 预计时间：1小时

- [ ] **任务2.5**: 实现SSH连接表单
  - 主机、端口、用户名
  - 认证方式（密码/密钥）
  - 密码输入框
  - 密钥文件选择
  - 预计时间：1.5小时

- [ ] **任务2.6**: 实现串口连接表单
  - 串口选择（使用mock platform获取）
  - 波特率、数据位、停止位、校验位
  - 预计时间：1小时

- [ ] **任务2.7**: 实现连接配置保存和加载
  - 保存到配置文件
  - 从配置文件加载
  - 预计时间：0.5小时

---

### Day 3: 设置对话框实现（8小时）

#### 上午（4小时）
- [ ] **任务3.1**: 创建`ui/settings_dialog.py`基础框架
  - 继承`QDialog`
  - 使用`QTabWidget`分类设置
  - 预计时间：1小时

- [ ] **任务3.2**: 实现终端设置页
  - 字体选择
  - 字体大小
  - 颜色方案选择
  - 滚动行数
  - 预计时间：1.5小时

- [ ] **任务3.3**: 实现快捷键设置页
  - 显示当前快捷键列表
  - 编辑快捷键
  - 恢复默认快捷键
  - 预计时间：1.5小时

#### 下午（4小时）
- [ ] **任务3.4**: 实现快捷指令设置页
  - 显示快捷指令列表
  - 添加/编辑/删除快捷指令
  - 设置快捷键
  - 预计时间：2小时

- [ ] **任务3.5**: 实现应用设置页
  - 语言选择
  - 主题选择
  - 启动时恢复会话
  - 预计时间：1小时

- [ ] **任务3.6**: 实现设置保存和应用
  - 保存到配置文件
  - 应用设置到主窗口
  - 预计时间：1小时

---

### Day 4: 文件传输客户端实现（8小时）

#### 上午（4小时）
- [ ] **任务4.1**: 创建`file_transfer/sftp_client.py`基础框架
  - 定义`SFTPClient`类
  - 初始化paramiko SFTP
  - 预计时间：1小时

- [ ] **任务4.2**: 实现SFTP连接
  - 从SSH连接创建SFTP会话
  - 实现`connect()`方法
  - 预计时间：1小时

- [ ] **任务4.3**: 实现文件上传
  - 实现`upload(local_path, remote_path, progress_callback)`
  - 支持进度回调
  - 处理上传异常
  - 预计时间：1.5小时

- [ ] **任务4.4**: 实现文件下载
  - 实现`download(remote_path, local_path, progress_callback)`
  - 支持进度回调
  - 处理下载异常
  - 预计时间：0.5小时

#### 下午（4小时）
- [ ] **任务4.5**: 实现目录操作
  - 列出目录：`list_dir(path)`
  - 创建目录：`mkdir(path)`
  - 删除文件/目录：`remove(path)`, `rmdir(path)`
  - 重命名：`rename(old, new)`
  - 预计时间：2小时

- [ ] **任务4.6**: 实现文件信息获取
  - 获取文件属性：`stat(path)`
  - 判断是否为目录：`isdir(path)`
  - 预计时间：1小时

- [ ] **任务4.7**: SFTP客户端单元测试
  - 测试上传下载
  - 测试目录操作
  - 预计时间：1小时

---

### Day 5: 文件浏览器UI实现（8小时）

#### 上午（4小时）
- [ ] **任务5.1**: 创建`file_transfer/file_browser.py`基础框架
  - 继承`QWidget`
  - 双面板布局（本地/远程）
  - 预计时间：1小时

- [ ] **任务5.2**: 实现本地文件浏览器
  - 使用`QTreeView`或`QListView`
  - 显示文件列表
  - 支持目录导航
  - 预计时间：1.5小时

- [ ] **任务5.3**: 实现远程文件浏览器
  - 使用SFTP客户端获取文件列表
  - 显示文件列表
  - 支持目录导航
  - 预计时间：1.5小时

#### 下午（4小时）
- [ ] **任务5.4**: 实现文件传输操作
  - 拖拽上传/下载
  - 右键菜单（上传、下载、删除、重命名）
  - 预计时间：2小时

- [ ] **任务5.5**: 实现传输进度显示
  - 进度条显示
  - 传输速度显示
  - 支持取消传输
  - 预计时间：1.5小时

- [ ] **任务5.6**: 文件浏览器样式优化
  - 图标显示
  - 文件大小格式化
  - 预计时间：0.5小时

---

### Day 6: 移除mock + 集成测试（8小时）

#### 上午（4小时）
- [ ] **任务6.1**: 移除platform mock
  - 将`from tests.mock_platform import MockPlatform`
  - 改为`from platform.factory import get_platform`
  - 测试与真实platform接口的集成
  - 预计时间：1小时

- [ ] **任务6.2**: 移除terminal mock
  - 将`from tests.mock_terminal import MockTerminalWidget`
  - 改为`from terminal.terminal_widget import TerminalWidget`
  - 测试与真实terminal组件的集成
  - 预计时间：1小时

- [ ] **任务6.3**: 移除connection mock
  - 使用真实的`SSHConnection`和`SerialConnection`
  - 测试连接功能
  - 预计时间：1小时

- [ ] **任务6.4**: 集成测试 - SSH连接
  - 通过UI创建SSH连接
  - 测试终端交互
  - 测试文件传输
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务6.5**: 集成测试 - 串口连接
  - 通过UI创建串口连接
  - 测试终端交互
  - 预计时间：1小时

- [ ] **任务6.6**: 集成测试 - 快捷键和快捷指令
  - 测试所有快捷键
  - 测试快捷指令执行
  - 预计时间：1小时

- [ ] **任务6.7**: 集成测试 - 多标签管理
  - 测试多个会话同时运行
  - 测试标签切换
  - 测试标签关闭
  - 预计时间：1小时

- [ ] **任务6.8**: 跨平台测试
  - 在Windows上测试
  - 在Linux上测试
  - 修复平台特定bug
  - 预计时间：1小时

---

### Day 7: 完善功能 + 合入master（8小时）

#### 上午（4小时）
- [ ] **任务7.1**: UI优化和美化
  - 调整布局和间距
  - 优化颜色和字体
  - 添加图标
  - 预计时间：1.5小时

- [ ] **任务7.2**: 错误处理和用户提示
  - 连接失败提示
  - 文件传输失败提示
  - 输入验证
  - 预计时间：1.5小时

- [ ] **任务7.3**: 补充单元测试
  - 确保测试覆盖率 > 70%
  - 修复测试失败的用例
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务7.4**: 用户体验优化
  - 添加快捷键提示
  - 优化对话框交互
  - 添加加载动画
  - 预计时间：1.5小时

- [ ] **任务7.5**: 文档完善
  - 更新接口文档
  - 添加使用示例
  - 编写用户手册
  - 预计时间：1小时

- [ ] **任务7.6**: 代码最终审查
  - 检查代码规范
  - 移除调试代码
  - 优化性能
  - 预计时间：0.5小时

- [ ] **任务7.7**: 合入master
  - 提交所有代码
  - 合并到master分支
  - 通知团队集成完成
  - 预计时间：1小时

---

## 📦 交付物清单

### 代码文件
- [ ] `ui/main_window.py`
- [ ] `ui/connection_dialog.py`
- [ ] `ui/settings_dialog.py`
- [ ] `ui/session_tab.py`
- [ ] `ui/__init__.py`
- [ ] `file_transfer/sftp_client.py`
- [ ] `file_transfer/file_browser.py`
- [ ] `file_transfer/__init__.py`

### 测试文件
- [ ] `tests/test_main_window.py`
- [ ] `tests/test_connection_dialog.py`
- [ ] `tests/test_settings_dialog.py`
- [ ] `tests/test_sftp_client.py`
- [ ] `tests/test_file_browser.py`

### 文档
- [ ] 接口文档（docstring）
- [ ] 用户手册
- [ ] 使用示例

---

## ✅ 合入master检查清单

在Day 7合入master前，请确认以下所有项：

- [ ] 所有代码文件已创建并实现
- [ ] 所有单元测试通过（覆盖率 > 70%）
- [ ] UI功能测试通过（连接、设置、多标签）
- [ ] 文件传输测试通过（上传、下载、进度显示）
- [ ] 快捷键功能测试通过
- [ ] 已移除所有mock，使用真实接口
- [ ] 在Windows和Linux上测试通过
- [ ] 代码符合PEP 8规范
- [ ] 所有公共接口都有docstring
- [ ] 没有遗留的TODO或FIXME
- [ ] 代码已提交到`feature/ui-filetransfer`分支
- [ ] 已通过自我代码审查

---

## 🔧 开发环境要求

### 必需工具
- Python 3.8+
- Git
- pytest（测试框架）
- Qt Designer（可选，用于UI设计）

### 依赖包
```bash
pip install PyQt5
pip install paramiko
```

### 测试环境
- SSH服务器（用于测试文件传输）
- 测试文件（用于上传下载测试）

---

## 📞 协作要点

### 与开发人员A的协作
- Day 1-5: 使用`tests/mock_platform.py`模拟platform接口
- Day 6: A完成后，切换到真实platform接口
- 使用platform.ui获取默认字体和快捷键修饰符
- 使用platform.clipboard实现复制粘贴
- 使用platform.filesystem打开文件管理器

### 与开发人员B的协作
- Day 1-5: 使用`tests/mock_terminal.py`和mock connection
- Day 6: B完成后，切换到真实接口
- 使用TerminalWidget显示终端
- 使用SSHConnection和SerialConnection管理连接
- 使用CommandExecutor执行快捷指令

### 合入后的工作
- Day 7合入后，所有模块集成完成
- Day 8-9参与集成测试和bug修复
- Day 10参与最终验收

---

## 🚨 风险与应对

### 风险1: UI布局复杂度超出预期
- **应对**: 使用Qt Designer辅助设计，优先实现核心功能
- **预留时间**: Day 7上午有1.5小时用于UI优化

### 风险2: 文件传输性能问题
- **应对**: 使用多线程传输，添加传输队列
- **实现**: 在`sftp_client.py`中使用`QThread`

### 风险3: 跨平台UI兼容性问题
- **应对**: 使用PyQt5的跨平台特性，避免平台特定代码
- **测试**: Day 6下午进行跨平台测试

### 风险4: Mock切换到真实接口时出现问题
- **应对**: 提前与A和B沟通接口细节，确保接口契约一致
- **预留时间**: Day 6上午有3小时用于移除mock和集成测试

---

## 📊 进度跟踪

| Day | 计划任务 | 完成状态 | 实际耗时 | 备注 |
|-----|---------|---------|---------|------|
| Day 1 | 主窗口框架 | ⬜ | - | - |
| Day 2 | 会话标签 + 连接对话框 | ⬜ | - | - |
| Day 3 | 设置对话框 | ⬜ | - | - |
| Day 4 | SFTP客户端 | ⬜ | - | - |
| Day 5 | 文件浏览器 | ⬜ | - | - |
| Day 6 | 移除mock + 集成测试 | ⬜ | - | - |
| Day 7 | 完善功能 + 合入 | ⬜ | - | - |

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
# Day 1-5: 使用mock
from tests.mock_platform import get_mock_platform
from tests.mock_terminal import MockTerminalWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.platform = get_mock_platform()
        self.terminal = MockTerminalWidget()

# Day 6: 切换到真实接口
from platform.factory import get_platform
from terminal.terminal_widget import TerminalWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.platform = get_platform()
        self.terminal = TerminalWidget()
```

### 创建SSH会话示例
```python
from core.ssh_connection import SSHConnection
from terminal.terminal_widget import TerminalWidget
from ui.session_tab import SessionTab

# 创建连接
ssh = SSHConnection()
ssh.on_data_received = terminal.write_output
ssh.on_connection_changed = self.update_status

# 连接终端
terminal.data_to_send.connect(ssh.send)

# 创建会话标签
tab = SessionTab(connection=ssh, terminal=terminal)
self.tabs.addTab(tab, "SSH - 192.168.1.100")

# 连接
ssh.connect(host="192.168.1.100", port=22, username="root", password="password")
```

### 文件传输示例
```python
from file_transfer.sftp_client import SFTPClient

# 创建SFTP客户端
sftp = SFTPClient(ssh_connection)
sftp.connect()

# 上传文件
def on_progress(transferred, total):
    progress = int(transferred / total * 100)
    print(f"上传进度: {progress}%")

sftp.upload("/local/file.txt", "/remote/file.txt", on_progress)
```

---

## 🎨 UI设计参考

### 主窗口布局
```
┌─────────────────────────────────────────────┐
│ 文件(F)  编辑(E)  视图(V)  帮助(H)           │ 菜单栏
├─────────────────────────────────────────────┤
│ [新建] [断开] [设置]                         │ 工具栏
├─────────────────────────────────────────────┤
│ ┌─────┬─────┬─────┐                         │
│ │SSH-1│SSH-2│COM3 │ ...                     │ 标签页
│ ├─────┴─────┴─────┴─────────────────────────┤
│ │                                           │
│ │         终端显示区域                       │
│ │                                           │
│ │                                           │
│ └───────────────────────────────────────────┘
├─────────────────────────────────────────────┤
│ 已连接 | 192.168.1.100:22 | root            │ 状态栏
└─────────────────────────────────────────────┘
```

### 连接对话框布局
```
┌─────────────────────────────────────┐
│ 新建连接                             │
├─────────────────────────────────────┤
│ 连接类型: [SSH ▼]                   │
│                                     │
│ 主机: [________________]            │
│ 端口: [22__]                        │
│ 用户名: [________________]          │
│                                     │
│ 认证方式: ○ 密码  ○ 密钥            │
│ 密码: [________________]            │
│                                     │
│         [连接]  [取消]              │
└─────────────────────────────────────┘
```

---

**祝开发顺利！你的模块是用户直接接触的界面，加油！** 🚀
