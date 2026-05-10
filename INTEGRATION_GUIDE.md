# MShell 集成版本使用说明

## 概述

MShell 是一个跨平台终端工具，支持SSH和串口连接、ANSI颜色渲染、快捷指令和文件传输。

## 已集成的模块

### ✅ 核心模块
- **Platform** - 平台适配层（Windows/Linux/macOS）
- **Config** - 配置管理
- **Terminal** - 终端渲染引擎（ANSI颜色支持）
- **Core** - 连接管理（SSH/串口）
- **File Transfer** - 文件传输（SFTP）

### 🎨 功能特性
- ✓ SSH连接（密码/密钥认证）
- ✓ 串口连接（多种波特率）
- ✓ ANSI颜色渲染（16色/256色/RGB）
- ✓ 多标签会话管理
- ✓ 快捷指令执行
- ✓ 颜色方案切换（default/solarized_dark/monokai/dracula）

## 运行方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行程序
```bash
python3 main.py
```

### 3. 使用说明

#### SSH连接
1. 点击"SSH连接"按钮
2. 输入主机地址（如：localhost 或 192.168.1.100）
3. 输入用户名（如：root）
4. 输入密码
5. 连接成功后会创建新的终端标签页

#### 串口连接
1. 点击"串口连接"按钮
2. 从列表中选择串口设备（如：/dev/ttyUSB0 或 COM3）
3. 连接成功后会创建新的终端标签页（默认波特率115200）

#### 终端操作
- 支持所有标准键盘输入
- 支持方向键、Home、End、PageUp、PageDown
- 支持Ctrl组合键（Ctrl+C、Ctrl+D、Ctrl+L等）
- 自动ANSI颜色渲染
- 滚动历史记录（10000行）

## 目录结构

```
mshell/
├── main.py                 # 主程序（已集成所有模块）
├── platform/               # 平台适配层
│   ├── base/              # 抽象接口
│   ├── windows/           # Windows实现
│   ├── linux/             # Linux实现
│   ├── macos/             # macOS实现
│   └── factory.py         # 平台工厂
├── config/                # 配置管理
│   ├── config_manager.py  # 配置管理器
│   └── default_config.yaml # 默认配置
├── terminal/              # 终端渲染引擎
│   ├── ansi_parser.py     # ANSI解析器
│   ├── color_scheme.py    # 颜色方案
│   └── terminal_widget.py # 终端组件
├── core/                  # 连接管理
│   ├── connection_manager.py  # 抽象基类
│   ├── ssh_connection.py      # SSH连接
│   ├── serial_connection.py   # 串口连接
│   └── command_executor.py    # 快捷指令
├── file_transfer/         # 文件传输
│   ├── sftp_client.py     # SFTP客户端
│   └── file_browser.py    # 文件浏览器
└── tests/                 # 测试文件
```

## 配置文件

配置文件位置：
- **Linux**: `~/.config/mshell/config.yaml`
- **macOS**: `~/Library/Application Support/MShell/config.yaml`
- **Windows**: `%APPDATA%\MShell\config.yaml`

首次运行会自动创建默认配置。

## 测试

运行所有测试：
```bash
# 核心模块测试
PYTHONPATH=. python3 tests/test_core_modules.py

# 平台适配层测试
PYTHONPATH=. python3 tests/simple_test.py

# 配置管理测试
PYTHONPATH=. python3 tests/test_config_manager.py

# 文件传输测试
PYTHONPATH=. python3 tests/test_file_transfer.py
```

## 开发状态

| 模块 | 状态 | 负责人 |
|------|------|--------|
| Platform | ✅ 完成 | 开发人员A |
| Config | ✅ 完成 | 开发人员A |
| Terminal | ✅ 完成 | 开发人员B |
| Core | ✅ 完成 | 开发人员B |
| File Transfer | ✅ 完成 | 开发人员C |
| UI (简化版) | ✅ 完成 | 集成版本 |

## 技术栈

- **Python**: 3.8+
- **GUI**: PyQt5
- **SSH**: paramiko
- **串口**: pyserial
- **配置**: PyYAML

## 已知限制

1. 当前版本为简化的集成版本，UI功能较基础
2. 文件传输功能需要在SSH连接建立后才能使用
3. 在SSH远程环境下无法显示GUI（需要X11转发或本地运行）

## 下一步计划

- [ ] 完善UI模块（连接管理对话框、设置对话框）
- [ ] 集成文件传输UI
- [ ] 添加快捷键支持
- [ ] 添加会话保存/恢复功能
- [ ] 性能优化

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue。
