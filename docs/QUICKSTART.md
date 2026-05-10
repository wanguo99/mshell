# MShell - 快速开始指南

## 🎯 项目已准备就绪！

基础框架已完全搭建完成，三个开发人员现在可以立即开始并行开发。

## 📋 开发前检查清单

### 1. 环境准备
```bash
# 克隆项目（如果还没有）
cd mshell

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 确认你的角色

#### 👤 我是开发人员A
- **负责模块**: `platform/`, `config/`
- **创建分支**: `git checkout -b feature/platform-adapter`
- **阅读文档**: `docs/DEVELOPMENT_GUIDE.md` 的"开发人员A"部分
- **开始文件**: `platform/base/serial.py`

#### 👤 我是开发人员B
- **负责模块**: `terminal/`, `core/`
- **创建分支**: `git checkout -b feature/terminal-core`
- **阅读文档**: `docs/DEVELOPMENT_GUIDE.md` 的"开发人员B"部分
- **开始文件**: `terminal/ansi_parser.py`
- **使用Mock**: `from tests.mock_platform import get_mock_platform`

#### 👤 我是开发人员C
- **负责模块**: `ui/`, `file_transfer/`
- **创建分支**: `git checkout -b feature/ui-filetransfer`
- **阅读文档**: `docs/DEVELOPMENT_GUIDE.md` 的"开发人员C"部分
- **开始文件**: `ui/main_window.py`
- **使用Mock**: `from tests.mock_platform import get_mock_platform`
                `from tests.mock_terminal import MockTerminalWidget`

## 📚 必读文档（按顺序）

1. **README.md** (5分钟) - 了解项目概述
2. **CLAUDE.md** (10分钟) - 了解完整架构
3. **docs/INTERFACE_CONTRACT.md** (15分钟) - 了解接口契约 ⭐ 重要！
4. **docs/DEVELOPMENT_GUIDE.md** (20分钟) - 了解你的开发任务

## 🚀 立即开始

### 开发人员A - 第一步

```bash
# 创建第一个文件
touch platform/base/serial.py

# 编辑文件，实现SerialBase基类
# 参考 docs/INTERFACE_CONTRACT.md 中的接口定义
```

### 开发人员B - 第一步

```bash
# 创建第一个文件
touch terminal/ansi_parser.py

# 使用Mock平台
# from tests.mock_platform import get_mock_platform
```

### 开发人员C - 第一步

```bash
# 创建第一个文件
touch ui/main_window.py

# 使用Mock
# from tests.mock_platform import get_mock_platform
# from tests.mock_terminal import MockTerminalWidget
```

## 💡 开发提示

### 使用Mock的示例

```python
# 在开发阶段
from tests.mock_platform import get_mock_platform

class MyClass:
    def __init__(self):
        # 使用Mock，不依赖真实的platform模块
        self.platform = get_mock_platform()
        
        # 现在可以调用platform接口
        ports = self.platform.serial.get_available_ports()
        print(f"可用串口: {ports}")
```

### 接口契约示例

```python
# 如果你是B，需要使用A提供的接口
# 参考 docs/INTERFACE_CONTRACT.md 中的定义

from platform.factory import get_platform  # 集成后
# from tests.mock_platform import get_mock_platform  # 开发时

platform = get_platform()
ports = platform.serial.get_available_ports()
```

## 🔄 开发流程

```
1. 独立开发 (5-6天)
   ├─ 使用Mock模拟依赖
   ├─ 实现自己的模块
   ├─ 编写单元测试
   └─ 提交到自己的分支

2. 集成阶段 (2-3天)
   ├─ A完成 → B和C移除platform mock
   ├─ B完成 → C移除terminal mock
   ├─ 端到端测试
   └─ 跨平台测试

3. 完成 🎉
```

## 📞 遇到问题？

### 常见问题

**Q: 我需要的接口还没实现怎么办？**
A: 使用 `tests/mock_*.py` 中的Mock类

**Q: 接口定义不清楚怎么办？**
A: 查看 `docs/INTERFACE_CONTRACT.md`

**Q: 不知道从哪里开始？**
A: 查看 `docs/DEVELOPMENT_GUIDE.md` 对应你角色的部分

**Q: 需要修改接口怎么办？**
A: 先在团队中讨论，然后更新 `docs/INTERFACE_CONTRACT.md`

## ✅ 开发完成检查

### 开发人员A
- [ ] 所有base/接口基类已实现
- [ ] Windows平台实现完成
- [ ] Linux平台实现完成
- [ ] macOS平台实现完成
- [ ] platform/factory.py完成
- [ ] config/config_manager.py完成
- [ ] 单元测试通过

### 开发人员B
- [ ] terminal/terminal_widget.py完成
- [ ] terminal/ansi_parser.py完成
- [ ] terminal/color_scheme.py完成
- [ ] core/connection_manager.py完成
- [ ] core/ssh_connection.py完成
- [ ] core/serial_connection.py完成
- [ ] core/command_executor.py完成
- [ ] 单元测试通过

### 开发人员C
- [ ] ui/main_window.py完成
- [ ] ui/connection_dialog.py完成
- [ ] ui/settings_dialog.py完成
- [ ] ui/session_tab.py完成
- [ ] file_transfer/sftp_client.py完成
- [ ] file_transfer/file_browser.py完成
- [ ] 单元测试通过

## 🎉 准备好了吗？

**现在就开始吧！** 选择你的角色，创建分支，开始编码！

```bash
# 创建你的分支
git checkout -b feature/your-module

# 开始开发
# ... 编码 ...

# 提交代码
git add .
git commit -m "feat: 实现XXX功能"
git push origin feature/your-module
```

---

**祝开发顺利！** 🚀
