# MShell - 跨平台终端工具

一个类似Xshell的跨平台终端工具，支持SSH和串口连接、自定义快捷键、颜色渲染、快捷指令和文件传输功能。

## 功能特性

- ✅ SSH连接（密码和密钥认证）
- ✅ 串口连接（支持多种波特率和配置）
- ✅ ANSI颜色渲染
- ✅ 自定义快捷键
- ✅ 快捷指令管理
- ✅ SFTP文件传输（类似MobaXterm）
- ✅ 跨平台支持（Windows/Linux/macOS）
- ✅ 多标签会话管理

## 技术栈

- **Python**: 3.8+
- **GUI框架**: PyQt5
- **SSH**: paramiko
- **串口**: pyserial
- **配置**: PyYAML

## 项目结构

```
mshell/
├── main.py                      # 应用入口
├── requirements.txt             # 依赖清单
├── platform/                    # OS适配层（开发人员A）
│   ├── base/                    # 平台接口基类
│   ├── windows/                 # Windows平台实现
│   ├── linux/                   # Linux平台实现
│   ├── macos/                   # macOS平台实现
│   └── factory.py               # 平台工厂
├── config/                      # 配置管理（开发人员A）
│   ├── config_manager.py
│   └── default_config.yaml
├── core/                        # 连接管理（开发人员B）
│   ├── connection_manager.py
│   ├── ssh_connection.py
│   ├── serial_connection.py
│   └── command_executor.py
├── terminal/                    # 终端渲染（开发人员B）
│   ├── terminal_widget.py
│   ├── ansi_parser.py
│   └── color_scheme.py
├── ui/                          # 用户界面（开发人员C）
│   ├── main_window.py
│   ├── connection_dialog.py
│   ├── settings_dialog.py
│   └── session_tab.py
├── file_transfer/               # 文件传输（开发人员C）
│   ├── sftp_client.py
│   └── file_browser.py
├── tests/                       # 测试
└── docs/                        # 文档
    ├── INTERFACE_CONTRACT.md    # 接口契约
    └── DEVELOPMENT_GUIDE.md     # 开发指南
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

## 并行开发指南

本项目采用三人并行开发模式，详细信息请参考：

- **接口契约**: [docs/INTERFACE_CONTRACT.md](docs/INTERFACE_CONTRACT.md)
- **开发指南**: [docs/DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md)

### 开发人员分工

#### 👤 开发人员A：平台适配层 + 配置管理
- 负责模块：`platform/`, `config/`
- 工作量：4-5天
- 依赖：无，可独立开发

#### 👤 开发人员B：终端核心 + 连接管理
- 负责模块：`terminal/`, `core/`
- 工作量：5-6天
- 依赖：A的platform接口（可先用mock）

#### 👤 开发人员C：UI界面 + 文件传输
- 负责模块：`ui/`, `file_transfer/`
- 工作量：5-6天
- 依赖：A和B的接口（可先用mock）

### 开发流程

1. **独立开发**（5-6天）
   - 各自按照接口契约开发
   - 使用mock模拟依赖
   - 编写单元测试

2. **集成阶段**（2-3天）
   - 移除mock，集成真实模块
   - 端到端测试
   - 跨平台测试

## 分支策略

```
main
├── feature/platform-adapter    # 开发人员A
├── feature/terminal-core       # 开发人员B
└── feature/ui-filetransfer     # 开发人员C
```

## 配置文件示例

```yaml
connections:
  - name: "服务器1"
    type: "ssh"
    host: "192.168.1.100"
    port: 22
    username: "root"
    auth_type: "password"
    
  - name: "串口设备"
    type: "serial"
    port: "COM3"
    baudrate: 115200

shortcuts:
  "Ctrl+T": "new_tab"
  "Ctrl+W": "close_tab"
  "Ctrl+Shift+C": "copy"
  "Ctrl+Shift+V": "paste"

quick_commands:
  - name: "系统信息"
    command: "uname -a"
    shortcut: "F1"

terminal:
  font_family: "Consolas"
  font_size: 12
  color_scheme: "default"
  scrollback_lines: 1000
```

## 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定模块测试
python -m pytest tests/test_platform.py
python -m pytest tests/test_terminal.py
python -m pytest tests/test_ui.py
```

## 贡献指南

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

- 项目地址：[GitHub Repository]
- 问题反馈：[Issues]
