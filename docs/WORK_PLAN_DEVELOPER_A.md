# 开发人员A - 工作计划书

## 👤 基本信息

- **负责人**: 开发人员A
- **负责模块**: `platform/`, `config/`
- **特性分支**: `feature/platform-adapter`
- **工作周期**: Day 1 - Day 5（5个工作日）
- **合入时机**: Day 5（第一个合入master）
- **依赖关系**: 无依赖，可独立开发

---

## 🎯 工作目标

实现跨平台适配层（OSA）和配置管理模块，为其他开发人员提供统一的平台接口，屏蔽Windows/Linux/macOS的差异。

---

## 📋 详细任务清单

### Day 1: 接口基类设计与实现（8小时）

#### 上午（4小时）
- [ ] **任务1.1**: 创建`platform/base/serial.py`
  - 定义`SerialBase`抽象基类
  - 方法：`get_available_ports()`, `get_port_description()`
  - 预计时间：1小时

- [ ] **任务1.2**: 创建`platform/base/config.py`
  - 定义`ConfigBase`抽象基类
  - 方法：`get_config_dir()`, `get_data_dir()`, `get_cache_dir()`
  - 预计时间：1小时

- [ ] **任务1.3**: 创建`platform/base/clipboard.py`
  - 定义`ClipboardBase`抽象基类
  - 方法：`get_text()`, `set_text()`, `clear()`
  - 预计时间：1小时

- [ ] **任务1.4**: 创建`platform/base/filesystem.py`
  - 定义`FilesystemBase`抽象基类
  - 方法：`normalize_path()`, `open_file_manager()`, `get_home_dir()`
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务1.5**: 创建`platform/base/ui.py`
  - 定义`UIBase`抽象基类
  - 方法：`get_default_font()`, `get_shortcut_modifier()`, `get_theme()`
  - 预计时间：1小时

- [ ] **任务1.6**: 创建`platform/base/__init__.py`
  - 导出所有基类
  - 预计时间：0.5小时

- [ ] **任务1.7**: 编写接口文档和示例
  - 在每个基类中添加详细的docstring
  - 预计时间：1.5小时

- [ ] **任务1.8**: 代码审查和调整
  - 自我审查接口设计的合理性
  - 预计时间：1小时

---

### Day 2: Windows平台实现（8小时）

#### 上午（4小时）
- [ ] **任务2.1**: 实现`platform/windows/serial.py`
  - 使用`serial.tools.list_ports`枚举COM口
  - 实现`WindowsSerial`类
  - 预计时间：1.5小时

- [ ] **任务2.2**: 实现`platform/windows/config.py`
  - 配置路径：`%APPDATA%\MShell\`
  - 实现`WindowsConfig`类
  - 预计时间：1小时

- [ ] **任务2.3**: 实现`platform/windows/clipboard.py`
  - 使用`win32clipboard`或`pyperclip`
  - 实现`WindowsClipboard`类
  - 预计时间：1.5小时

#### 下午（4小时）
- [ ] **任务2.4**: 实现`platform/windows/filesystem.py`
  - 路径规范化（处理反斜杠）
  - 使用`os.startfile()`打开文件管理器
  - 实现`WindowsFilesystem`类
  - 预计时间：1.5小时

- [ ] **任务2.5**: 实现`platform/windows/ui.py`
  - 默认字体：Consolas, Courier New
  - 快捷键修饰符：Ctrl
  - 实现`WindowsUI`类
  - 预计时间：1小时

- [ ] **任务2.6**: 创建`platform/windows/__init__.py`
  - 导出所有Windows实现
  - 预计时间：0.5小时

- [ ] **任务2.7**: Windows平台测试
  - 在Windows上测试所有功能
  - 预计时间：1小时

---

### Day 3: Linux平台实现（8小时）

#### 上午（4小时）
- [ ] **任务3.1**: 实现`platform/linux/serial.py`
  - 枚举`/dev/ttyUSB*`, `/dev/ttyACM*`, `/dev/ttyS*`
  - 实现`LinuxSerial`类
  - 预计时间：1.5小时

- [ ] **任务3.2**: 实现`platform/linux/config.py`
  - 配置路径：`~/.config/mshell/`
  - 遵循XDG Base Directory规范
  - 实现`LinuxConfig`类
  - 预计时间：1小时

- [ ] **任务3.3**: 实现`platform/linux/clipboard.py`
  - 使用`pyperclip`或`xclip`
  - 实现`LinuxClipboard`类
  - 预计时间：1.5小时

#### 下午（4小时）
- [ ] **任务3.4**: 实现`platform/linux/filesystem.py`
  - 路径规范化（处理正斜杠）
  - 使用`xdg-open`打开文件管理器
  - 实现`LinuxFilesystem`类
  - 预计时间：1.5小时

- [ ] **任务3.5**: 实现`platform/linux/ui.py`
  - 默认字体：Monospace, DejaVu Sans Mono
  - 快捷键修饰符：Ctrl
  - 实现`LinuxUI`类
  - 预计时间：1小时

- [ ] **任务3.6**: 创建`platform/linux/__init__.py`
  - 导出所有Linux实现
  - 预计时间：0.5小时

- [ ] **任务3.7**: Linux平台测试
  - 在Linux上测试所有功能
  - 预计时间：1小时

---

### Day 4: macOS平台实现 + 平台工厂（8小时）

#### 上午（4小时）
- [ ] **任务4.1**: 实现`platform/macos/serial.py`
  - 枚举`/dev/tty.usbserial-*`, `/dev/cu.usbserial-*`
  - 实现`MacOSSerial`类
  - 预计时间：1.5小时

- [ ] **任务4.2**: 实现`platform/macos/config.py`
  - 配置路径：`~/Library/Application Support/MShell/`
  - 实现`MacOSConfig`类
  - 预计时间：1小时

- [ ] **任务4.3**: 实现`platform/macos/clipboard.py`
  - 使用`pyperclip`或`pbcopy/pbpaste`
  - 实现`MacOSClipboard`类
  - 预计时间：1.5小时

#### 下午（4小时）
- [ ] **任务4.4**: 实现`platform/macos/filesystem.py`
  - 使用`open`命令打开Finder
  - 实现`MacOSFilesystem`类
  - 预计时间：1小时

- [ ] **任务4.5**: 实现`platform/macos/ui.py`
  - 默认字体：Menlo, Monaco
  - 快捷键修饰符：Cmd (⌘)
  - 实现`MacOSUI`类
  - 预计时间：1小时

- [ ] **任务4.6**: 实现`platform/factory.py`
  - 根据`platform.system()`返回对应平台实例
  - 实现`Platform`类和`get_platform()`工厂函数
  - 预计时间：1.5小时

- [ ] **任务4.7**: 创建`platform/__init__.py`
  - 导出`get_platform`
  - 预计时间：0.5小时

---

### Day 5: 配置管理 + 测试 + 合入（8小时）

#### 上午（4小时）
- [ ] **任务5.1**: 实现`config/config_manager.py`
  - 实现`ConfigManager`类
  - 方法：`load()`, `save()`, `get()`, `set()`, `get_connections()`, `get_shortcuts()`
  - 预计时间：2小时

- [ ] **任务5.2**: 创建`config/default_config.yaml`
  - 定义默认配置结构
  - 包含示例连接、快捷键、终端设置等
  - 预计时间：1小时

- [ ] **任务5.3**: 编写单元测试
  - 测试所有平台接口
  - 测试配置管理器
  - 预计时间：1小时

#### 下午（4小时）
- [ ] **任务5.4**: 跨平台测试
  - 在Windows/Linux/macOS上运行测试
  - 修复平台特定的bug
  - 预计时间：2小时

- [ ] **任务5.5**: 代码审查和优化
  - 检查代码质量
  - 优化性能
  - 添加必要的注释
  - 预计时间：1小时

- [ ] **任务5.6**: 合入master
  - 提交所有代码
  - 合并到master分支
  - 通知开发人员B和C
  - 预计时间：1小时

---

## 📦 交付物清单

### 代码文件
- [ ] `platform/base/serial.py`
- [ ] `platform/base/config.py`
- [ ] `platform/base/clipboard.py`
- [ ] `platform/base/filesystem.py`
- [ ] `platform/base/ui.py`
- [ ] `platform/base/__init__.py`
- [ ] `platform/windows/serial.py`
- [ ] `platform/windows/config.py`
- [ ] `platform/windows/clipboard.py`
- [ ] `platform/windows/filesystem.py`
- [ ] `platform/windows/ui.py`
- [ ] `platform/windows/__init__.py`
- [ ] `platform/linux/serial.py`
- [ ] `platform/linux/config.py`
- [ ] `platform/linux/clipboard.py`
- [ ] `platform/linux/filesystem.py`
- [ ] `platform/linux/ui.py`
- [ ] `platform/linux/__init__.py`
- [ ] `platform/macos/serial.py`
- [ ] `platform/macos/config.py`
- [ ] `platform/macos/clipboard.py`
- [ ] `platform/macos/filesystem.py`
- [ ] `platform/macos/ui.py`
- [ ] `platform/macos/__init__.py`
- [ ] `platform/factory.py`
- [ ] `platform/__init__.py`
- [ ] `config/config_manager.py`
- [ ] `config/default_config.yaml`
- [ ] `config/__init__.py`

### 测试文件
- [ ] `tests/test_platform_windows.py`
- [ ] `tests/test_platform_linux.py`
- [ ] `tests/test_platform_macos.py`
- [ ] `tests/test_config_manager.py`

### 文档
- [ ] 接口文档（docstring）
- [ ] 使用示例

---

## ✅ 合入master检查清单

在Day 5合入master前，请确认以下所有项：

- [ ] 所有代码文件已创建并实现
- [ ] 所有单元测试通过（覆盖率 > 80%）
- [ ] 在Windows平台上测试通过
- [ ] 在Linux平台上测试通过
- [ ] 在macOS平台上测试通过（如果有条件）
- [ ] 代码符合PEP 8规范
- [ ] 所有公共接口都有docstring
- [ ] 没有遗留的TODO或FIXME
- [ ] 代码已提交到`feature/platform-adapter`分支
- [ ] 已通过自我代码审查

---

## 🔧 开发环境要求

### 必需工具
- Python 3.8+
- Git
- pytest（测试框架）

### 依赖包
```bash
pip install pyserial
pip install pyperclip  # 剪贴板支持
pip install PyYAML     # 配置文件
```

### 测试环境
- 至少在两个平台上测试（Windows + Linux 或 Windows + macOS）
- 如果没有多平台环境，可以使用虚拟机或Docker

---

## 📞 协作要点

### 与开发人员B的协作
- B需要使用你的`platform.serial`接口获取串口列表
- B需要使用你的`platform.config`接口获取配置路径
- 确保接口稳定，避免频繁修改

### 与开发人员C的协作
- C需要使用你的`platform.ui`接口获取默认字体和快捷键修饰符
- C需要使用你的`platform.clipboard`接口实现复制粘贴
- C需要使用你的`platform.filesystem`接口打开文件管理器

### 合入后的支持
- Day 5合入后，B和C会切换到真实接口
- 如果他们遇到接口问题，需要及时修复
- Day 6-7继续提供技术支持

---

## 🚨 风险与应对

### 风险1: 平台差异导致的兼容性问题
- **应对**: 充分测试，使用try-except处理平台特定异常
- **预留时间**: Day 5下午的2小时跨平台测试

### 风险2: 缺少某个平台的测试环境
- **应对**: 优先保证Windows和Linux，macOS可以让团队其他成员帮忙测试
- **备选方案**: 使用GitHub Actions进行跨平台CI测试

### 风险3: 第三方库（如pyperclip）在某些平台不工作
- **应对**: 准备降级方案，使用平台原生命令（如xclip, pbcopy）
- **实现**: 在clipboard实现中添加fallback逻辑

---

## 📊 进度跟踪

| Day | 计划任务 | 完成状态 | 实际耗时 | 备注 |
|-----|---------|---------|---------|------|
| Day 1 | 接口基类设计 | ⬜ | - | - |
| Day 2 | Windows平台实现 | ⬜ | - | - |
| Day 3 | Linux平台实现 | ⬜ | - | - |
| Day 4 | macOS平台实现 + 工厂 | ⬜ | - | - |
| Day 5 | 配置管理 + 测试 + 合入 | ⬜ | - | - |

---

## 📝 每日总结模板

### Day X 工作总结
- **完成任务**: 
- **遇到问题**: 
- **解决方案**: 
- **明天计划**: 
- **需要协助**: 

---

**祝开发顺利！你是第一个合入master的开发人员，加油！** 🚀
