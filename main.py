"""MShell V2 - 使用新架构的启动文件

核心改进：
1. 分层架构（领域层、应用层、基础设施层、表现层）
2. 事件驱动（EventBus 解耦模块通信）
3. 异步统一（asyncio + AsyncBridge）
4. 性能优化（脏行标记 + 按需渲染）

预期性能提升：
- CPU 占用降低 60%+
- 渲染延迟从 ~100ms 降至 <16ms
- 内存占用优化 30%+
"""

import sys
import os

# 设置 Python 字节码缓存目录
os.environ['PYTHONPYCACHEPREFIX'] = os.path.join(os.path.dirname(__file__), '.cache', 'pycache')

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# 导入新架构的主窗口
from presentation.main_window_v2 import MainWindowV2


def main():
    """主函数"""
    # 启用高 DPI 支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("MShell V2")
    app.setOrganizationName("MShell")

    # 创建主窗口（新架构）
    window = MainWindowV2()
    window.show()

    # 运行事件循环
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
