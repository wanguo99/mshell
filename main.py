#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MShell - 跨平台终端工具
支持SSH和串口连接、自定义快捷键、颜色渲染、快捷指令和文件传输
"""

import sys
from PyQt5.QtWidgets import QApplication


def main():
    """应用程序入口"""
    app = QApplication(sys.argv)
    app.setApplicationName("MShell")
    app.setOrganizationName("MShell")

    # TODO: 等待开发人员A完成platform模块后取消注释
    # from platform.factory import get_platform
    # platform = get_platform()

    # TODO: 等待开发人员C完成ui模块后取消注释
    # from ui.main_window import MainWindow
    # window = MainWindow(platform)
    # window.show()

    # 临时测试代码
    print("MShell - 基础框架已搭建")
    print("等待各模块开发完成...")
    print("\n开发人员分工:")
    print("  A: platform/ + config/")
    print("  B: terminal/ + core/")
    print("  C: ui/ + file_transfer/")
    print("\n请参考 docs/INTERFACE_CONTRACT.md 了解接口契约")

    return 0
    # sys.exit(app.exec_())


if __name__ == "__main__":
    sys.exit(main())
