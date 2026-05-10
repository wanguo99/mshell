# MShell 开发节点与合入策略

## 📅 开发时间线总览

```
Day 1-5:  开发人员A独立开发 platform + config
Day 1-6:  开发人员B独立开发 terminal + core（使用mock）
Day 1-7:  开发人员C独立开发 ui + file_transfer（使用mock）

Day 5:    ✅ 里程碑1 - A完成并合入master
Day 6:    ✅ 里程碑2 - B完成并合入master  
Day 7:    ✅ 里程碑3 - C完成并合入master
Day 8-9:  集成测试、跨平台测试、bug修复
Day 10:   最终验收、文档完善
```

---

## 🎯 三个关键里程碑

### 里程碑1: Day 5 - 开发人员A合入master

**合入内容**: `platform/` + `config/` 模块

**合入条件**:
- [ ] 所有`platform/base/`接口基类已实现
- [ ] Windows/Linux/macOS三个平台实现完成
- [ ] `platform/factory.py`工厂类完成
- [ ] `config/config_manager.py`配置管理器完成
- [ ] 单元测试通过（覆盖率 > 80%）
- [ ] 在至少两个平台上验证功能正常

**合入后操作**:
```bash
# 开发人员A执行
git checkout master
git merge feature/platform-adapter
git push origin master

# 通知团队
echo "✅ platform + config 模块已合入master"
```

**开发人员B和C需要执行**:
```bash
# 更新master
git checkout master
git pull origin master

# 合并到自己的分支
git checkout feature/your-module
git merge master

# 移除platform mock
# 将 from tests.mock_platform import get_mock_platform
# 改为 from platform.factory import get_platform

# 测试集成
python -m pytest tests/
```

---

### 里程碑2: Day 6 - 开发人员B合入master

**合入内容**: `terminal/` + `core/` 模块

**合入条件**:
- [ ] `terminal/`模块所有文件完成（terminal_widget, ansi_parser, color_scheme）
- [ ] `core/`模块所有文件完成（connection_manager, ssh_connection, serial_connection, command_executor）
- [ ] 已移除platform mock，使用真实platform接口
- [ ] SSH连接测试通过（连接真实服务器）
- [ ] 串口连接测试通过（使用虚拟串口或真实设备）
- [ ] ANSI颜色渲染测试通过
- [ ] 单元测试通过（覆盖率 > 75%）

**合入后操作**:
```bash
# 开发人员B执行
git checkout master
git merge feature/terminal-core
git push origin master

# 通知团队
echo "✅ terminal + core 模块已合入master"
```

**开发人员C需要执行**:
```bash
# 更新master
git checkout master
git pull origin master

# 合并到自己的分支
git checkout feature/ui-filetransfer
git merge master

# 移除terminal和connection mock
# 将 from tests.mock_terminal import MockTerminalWidget
# 改为 from terminal.terminal_widget import TerminalWidget
# 将 mock connection 改为真实的 SSHConnection/SerialConnection

# 测试集成
python -m pytest tests/
```

---

### 里程碑3: Day 7 - 开发人员C合入master

**合入内容**: `ui/` + `file_transfer/` 模块

**合入条件**:
- [ ] `ui/`模块所有文件完成（main_window, connection_dialog, settings_dialog, session_tab）
- [ ] `file_transfer/`模块所有文件完成（sftp_client, file_browser）
- [ ] 已移除所有mock，使用真实接口
- [ ] UI功能测试通过（连接、设置、多标签）
- [ ] 文件传输测试通过（上传、下载、进度显示）
- [ ] 快捷键功能测试通过
- [ ] 单元测试通过（覆盖率 > 70%）

**合入后操作**:
```bash
# 开发人员C执行
git checkout master
git merge feature/ui-filetransfer
git push origin master

# 通知团队
echo "✅ ui + file_transfer 模块已合入master"
echo "🎉 所有模块集成完成！"
```

**所有开发人员执行**:
```bash
# 切换到master开始集成测试
git checkout master
git pull origin master

# 运行完整测试
python -m pytest tests/

# 运行应用
python main.py
```

---

## 🔀 合入流程详解

### 标准合入流程

```bash
# 1. 确保本地代码最新并已提交
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

### 冲突解决策略

如果合并时出现冲突：

1. **查看冲突文件**:
```bash
git status
```

2. **手动解决冲突**:
- 打开冲突文件
- 查找`<<<<<<<`, `=======`, `>>>>>>>`标记
- 保留正确的代码，删除冲突标记

3. **标记为已解决**:
```bash
git add <冲突文件>
```

4. **完成合并**:
```bash
git commit -m "merge: 解决合并冲突"
```

---

## 📢 合入后通知模板

### 开发人员A合入后通知

```
✅ platform + config 模块已合入master

📌 开发人员B和C请执行以下操作：

1. 更新master分支：
   git checkout master
   git pull origin master

2. 合并到你的特性分支：
   git checkout feature/your-module
   git merge master

3. 移除platform mock：
   将代码中的：
   from tests.mock_platform import get_mock_platform
   改为：
   from platform.factory import get_platform

4. 测试集成：
   python -m pytest tests/

如有问题请及时反馈！
```

### 开发人员B合入后通知

```
✅ terminal + core 模块已合入master

📌 开发人员C请执行以下操作：

1. 更新master分支：
   git checkout master
   git pull origin master

2. 合并到你的特性分支：
   git checkout feature/ui-filetransfer
   git merge master

3. 移除terminal和connection mock：
   将代码中的：
   from tests.mock_terminal import MockTerminalWidget
   改为：
   from terminal.terminal_widget import TerminalWidget
   
   将mock connection改为真实的SSHConnection/SerialConnection

4. 测试集成：
   python -m pytest tests/

如有问题请及时反馈！
```

### 开发人员C合入后通知

```
✅ ui + file_transfer 模块已合入master
🎉 所有模块集成完成！

📌 所有开发人员请执行以下操作：

1. 切换到master分支：
   git checkout master
   git pull origin master

2. 运行完整测试：
   python -m pytest tests/

3. 运行应用验证：
   python main.py

4. 开始集成测试阶段（Day 8-9）

恭喜大家完成开发阶段！接下来进入集成测试和优化阶段。
```

---

## ⚠️ 注意事项

### 合入前检查

每个开发人员在合入master前必须：

1. **代码完整性检查**
   - 所有计划的功能已实现
   - 没有遗留的TODO或FIXME
   - 没有调试代码（print, console.log等）

2. **测试检查**
   - 所有单元测试通过
   - 测试覆盖率达标
   - 手动测试核心功能

3. **代码质量检查**
   - 符合PEP 8规范
   - 有完整的docstring
   - 代码结构清晰

4. **依赖检查**
   - 如果依赖其他模块，确保已移除mock
   - 与真实接口集成测试通过

### 合入后责任

合入master后，该开发人员需要：

1. **及时响应问题**
   - 其他开发人员集成时遇到问题要及时解决
   - 监控团队群消息

2. **提供技术支持**
   - 解答接口使用问题
   - 协助调试集成问题

3. **修复bug**
   - 如果发现自己模块的bug，及时修复
   - 修复后通知其他开发人员更新

---

## 🚨 紧急情况处理

### 如果合入后发现严重bug

```bash
# 1. 立即通知团队
echo "⚠️ 发现严重bug，暂停集成"

# 2. 创建hotfix分支
git checkout master
git checkout -b hotfix/bug-description

# 3. 修复bug
# 编辑代码...
git add .
git commit -m "fix: 修复XXX严重bug"

# 4. 合并回master
git checkout master
git merge hotfix/bug-description
git push origin master

# 5. 通知团队更新
echo "✅ bug已修复，请更新master"
```

### 如果需要回滚合入

```bash
# 1. 查看提交历史
git log --oneline

# 2. 回滚到合入前的提交
git revert <commit-hash>

# 3. 推送回滚
git push origin master

# 4. 通知团队
echo "⚠️ 已回滚XXX模块的合入，请更新master"
```

---

## 📊 进度跟踪表

| 里程碑 | 负责人 | 计划日期 | 实际日期 | 状态 | 备注 |
|--------|--------|---------|---------|------|------|
| 里程碑1 | 开发人员A | Day 5 | - | ⬜ 待完成 | platform + config |
| 里程碑2 | 开发人员B | Day 6 | - | ⬜ 待完成 | terminal + core |
| 里程碑3 | 开发人员C | Day 7 | - | ⬜ 待完成 | ui + file_transfer |
| 集成测试 | 全体 | Day 8-9 | - | ⬜ 待完成 | 跨平台测试 |
| 最终验收 | 全体 | Day 10 | - | ⬜ 待完成 | 文档完善 |

---

## 📝 每日站会模板

建议每天进行简短的站会（15分钟），同步进度：

### 站会内容

1. **昨天完成了什么**
2. **今天计划做什么**
3. **遇到什么阻碍**
4. **需要什么帮助**

### 站会时间建议

- 每天上午10:00或下午2:00
- 线上或线下均可
- 保持简短高效

---

**祝项目顺利完成！** 🚀
