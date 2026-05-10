# MShell - 项目结构总览

## 📁 目录结构

```
mshell/
├── 📄 main.py                          # 应用程序入口
├── 📄 requirements.txt                 # Python依赖包列表
├── 📄 .gitignore                       # Git忽略文件配置
├── 📄 README.md                        # 项目说明文档
│
├── 📁 platform/                        # OS适配层（开发人员A）
│   ├── 📄 __init__.py
│   ├── 📄 factory.py                   # 平台工厂（待实现）
│   ├── 📁 base/                        # 平台接口基类
│   │   ├── 📄 __init__.py
│   │   ├── 📄 serial.py                # 串口接口基类（待实现）
│   │   ├── 📄 config.py                # 配置接口基类（待实现）
│   │   ├── 📄 clipboard.py             # 剪贴板接口基类（待实现）
│   │   ├── 📄 filesystem.py            # 文件系统接口基类（待实现）
│   │   └── 📄 ui.py                    # UI接口基类（待实现）
│   ├── 📁 windows/                     # Windows平台实现
│   │   ├── 📄 __init__.py
│   │   ├── 📄 serial.py                # （待实现）
│   │   ├── 📄 config.py                # （待实现）
│   │   ├── 📄 clipboard.py             # （待实现）
│   │   ├── 📄 filesystem.py            # （待实现）
│   │   └── 📄 ui.py                    # （待实现）
│   ├── 📁 linux/                       # Linux平台实现
│   │   ├── 📄 __init__.py
│   │   └── ... (同Windows结构)
│   └── 📁 macos/                       # macOS平台实现
│       ├── 📄 __init__.py
│       └── ... (同Windows结构)
│
├── 📁 config/                          # 配置管理（开发人员A）
│   ├── 📄 __init__.py
│   ├── 📄 config_manager.py            # 配置管理器（待实现）
│   └── 📄 default_config.yaml          # 默认配置文件 ✅
│
├── 📁 core/                            # 连接管理（开发人员B）
│   ├── 📄 __init__.py
│   ├── 📄 connection_manager.py        # 连接管理基类（待实现）
│   ├── 📄 ssh_connection.py            # SSH连接实现（待实现）
│   ├── 📄 serial_connection.py         # 串口连接实现（待实现）
│   └── 📄 command_executor.py          # 快捷指令执行器（待实现）
│
├── 📁 terminal/                        # 终端渲染（开发人员B）
│   ├── 📄 __init__.py
│   ├── 📄 terminal_widget.py           # 终端显示组件（待实现）
│   ├── 📄 ansi_parser.py               # ANSI解析器（待实现）
│   └── 📄 color_scheme.py              # 颜色方案管理（待实现）
│
├── 📁 ui/                              # 用户界面（开发人员C）
│   ├── 📄 __init__.py
│   ├── 📄 main_window.py               # 主窗口（待实现）
│   ├── 📄 connection_dialog.py         # 连接配置对话框（待实现）
│   ├── 📄 settings_dialog.py           # 设置对话框（待实现）
│   └── 📄 session_tab.py               # 会话标签页（待实现）
│
├── 📁 file_transfer/                   # 文件传输（开发人员C）
│   ├── 📄 __init__.py
│   ├── 📄 sftp_client.py               # SFTP客户端（待实现）
│   └── 📄 file_browser.py              # 文件浏览器UI（待实现）
│
├── 📁 tests/                           # 测试和Mock
│   ├── 📄 __init__.py
│   ├── 📄 mock_platform.py             # Mock平台接口 ✅
│   └── 📄 mock_terminal.py             # Mock终端和连接 ✅
│
└── 📁 docs/                            # 文档
    ├── 📄 INTERFACE_CONTRACT.md        # 接口契约文档 ✅
    └── 📄 DEVELOPMENT_GUIDE.md         # 开发指南 ✅
```

## ✅ 已完成

- [x] 项目目录结构
- [x] requirements.txt
- [x] 所有模块的__init__.py
- [x] main.py入口文件
- [x] README.md
- [x] .gitignore
- [x] 接口契约文档 (INTERFACE_CONTRACT.md)
- [x] 开发指南 (DEVELOPMENT_GUIDE.md)
- [x] Mock文件 (mock_platform.py, mock_terminal.py)
- [x] 默认配置文件 (default_config.yaml)

## 🚧 待开发

### 开发人员A的任务
- [ ] platform/base/ 所有接口基类
- [ ] platform/windows/ 所有实现
- [ ] platform/linux/ 所有实现
- [ ] platform/macos/ 所有实现
- [ ] platform/factory.py
- [ ] config/config_manager.py

### 开发人员B的任务
- [ ] terminal/terminal_widget.py
- [ ] terminal/ansi_parser.py
- [ ] terminal/color_scheme.py
- [ ] core/connection_manager.py
- [ ] core/ssh_connection.py
- [ ] core/serial_connection.py
- [ ] core/command_executor.py

### 开发人员C的任务
- [ ] ui/main_window.py
- [ ] ui/connection_dialog.py
- [ ] ui/settings_dialog.py
- [ ] ui/session_tab.py
- [ ] file_transfer/sftp_client.py
- [ ] file_transfer/file_browser.py

## 📚 关键文档

1. **README.md** - 项目概述和快速开始
2. **docs/INTERFACE_CONTRACT.md** - 模块间接口契约（必读！）
3. **docs/DEVELOPMENT_GUIDE.md** - 详细开发指南
4. **config/default_config.yaml** - 配置文件示例

## 🚀 开始开发

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 选择你的角色
- **开发人员A**: 创建分支 `feature/platform-adapter`
- **开发人员B**: 创建分支 `feature/terminal-core`
- **开发人员C**: 创建分支 `feature/ui-filetransfer`

### 3. 阅读文档
- 仔细阅读 `docs/INTERFACE_CONTRACT.md` 了解接口定义
- 参考 `docs/DEVELOPMENT_GUIDE.md` 了解开发流程

### 4. 使用Mock
- 在依赖模块未完成前，使用 `tests/mock_*.py` 中的Mock类
- 示例：
  ```python
  from tests.mock_platform import get_mock_platform
  platform = get_mock_platform()
  ```

### 5. 开发流程
1. 独立开发（使用Mock模拟依赖）
2. 编写单元测试
3. 提交代码到自己的分支
4. 等待其他模块完成
5. 集成测试（移除Mock）
6. 合并到主分支

## 📞 协作方式

- **接口变更**: 必须通知所有开发人员并更新接口契约文档
- **问题讨论**: 在团队群或Issues中讨论
- **代码审查**: 提交PR前进行自我审查

## 🎯 预期时间线

- **独立开发**: 5-6天
- **集成测试**: 2-3天
- **总计**: 7-9天（并行开发）

---

**现在可以开始并行开发了！** 🎉
