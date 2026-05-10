"""文件浏览器UI模块

提供本地和远程文件浏览、传输功能
"""

import os
from typing import Optional, Callable
from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QProgressBar, QMessageBox, QInputDialog,
    QSplitter, QMenu, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QIcon

from file_transfer.sftp_client import SFTPClient, FileInfo


class FileTransferThread(QThread):
    """文件传输线程"""

    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, operation: str, sftp_client: SFTPClient,
                 local_path: str, remote_path: str):
        super().__init__()
        self.operation = operation
        self.sftp_client = sftp_client
        self.local_path = local_path
        self.remote_path = remote_path

    def run(self):
        try:
            if self.operation == "upload":
                success = self.sftp_client.upload(
                    self.local_path, self.remote_path,
                    progress_callback=self.progress.emit
                )
                msg = "上传成功" if success else "上传失败"
            elif self.operation == "download":
                success = self.sftp_client.download(
                    self.remote_path, self.local_path,
                    progress_callback=self.progress.emit
                )
                msg = "下载成功" if success else "下载失败"
            else:
                success = False
                msg = "未知操作"

            self.finished.emit(success, msg)

        except Exception as e:
            self.finished.emit(False, f"传输失败: {str(e)}")


class FileListWidget(QTreeWidget):
    """文件列表组件"""

    file_double_clicked = pyqtSignal(str, bool)

    def __init__(self, is_remote: bool = False, parent=None):
        super().__init__(parent)
        self.is_remote = is_remote
        self.current_path = str(Path.home()) if not is_remote else "/"

        self.setHeaderLabels(["名称", "大小", "修改时间", "权限"])
        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 100)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)

    def set_files(self, files: list):
        """设置文件列表

        Args:
            files: FileInfo列表或本地文件路径列表
        """
        self.clear()

        # 添加上级目录项
        parent_item = QTreeWidgetItem(self)
        parent_item.setText(0, "..")
        parent_item.setData(0, Qt.UserRole, "..")
        parent_item.setData(1, Qt.UserRole, True)

        for file in files:
            item = QTreeWidgetItem(self)

            if isinstance(file, FileInfo):
                # 远程文件
                item.setText(0, file.name)
                item.setText(1, self._format_size(file.size) if not file.is_dir else "")
                item.setText(2, self._format_time(file.mtime))
                item.setText(3, file.permissions)
                item.setData(0, Qt.UserRole, file.name)
                item.setData(1, Qt.UserRole, file.is_dir)
            else:
                # 本地文件
                file_path = os.path.join(self.current_path, file)
                is_dir = os.path.isdir(file_path)
                item.setText(0, file)

                if not is_dir:
                    try:
                        size = os.path.getsize(file_path)
                        item.setText(1, self._format_size(size))
                    except:
                        item.setText(1, "")

                try:
                    mtime = os.path.getmtime(file_path)
                    item.setText(2, self._format_time(mtime))
                except:
                    item.setText(2, "")

                item.setData(0, Qt.UserRole, file)
                item.setData(1, Qt.UserRole, is_dir)

    def get_selected_file(self) -> tuple:
        """获取选中的文件

        Returns:
            (文件名, 是否目录)
        """
        items = self.selectedItems()
        if not items:
            return None, False

        item = items[0]
        filename = item.data(0, Qt.UserRole)
        is_dir = item.data(1, Qt.UserRole)
        return filename, is_dir

    def _on_item_double_clicked(self, item, column):
        """双击事件"""
        filename = item.data(0, Qt.UserRole)
        is_dir = item.data(1, Qt.UserRole)
        self.file_double_clicked.emit(filename, is_dir)

    def _show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)

        if self.is_remote:
            download_action = menu.addAction("下载")
            delete_action = menu.addAction("删除")
            rename_action = menu.addAction("重命名")
            menu.addSeparator()
            mkdir_action = menu.addAction("新建文件夹")

            action = menu.exec_(self.viewport().mapToGlobal(position))

            if action == download_action:
                self._emit_action("download")
            elif action == delete_action:
                self._emit_action("delete")
            elif action == rename_action:
                self._emit_action("rename")
            elif action == mkdir_action:
                self._emit_action("mkdir")
        else:
            upload_action = menu.addAction("上传")
            delete_action = menu.addAction("删除")
            rename_action = menu.addAction("重命名")

            action = menu.exec_(self.viewport().mapToGlobal(position))

            if action == upload_action:
                self._emit_action("upload")
            elif action == delete_action:
                self._emit_action("delete")
            elif action == rename_action:
                self._emit_action("rename")

    def _emit_action(self, action: str):
        """触发操作信号"""
        # 由父组件处理
        pass

    @staticmethod
    def _format_size(size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    @staticmethod
    def _format_time(timestamp: float) -> str:
        """格式化时间"""
        from datetime import datetime
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return ""


class FileBrowser(QWidget):
    """文件浏览器主组件"""

    def __init__(self, sftp_client: Optional[SFTPClient] = None, parent=None):
        super().__init__(parent)
        self.sftp_client = sftp_client
        self.transfer_thread = None

        self._init_ui()
        self._refresh_local()
        if self.sftp_client:
            self._refresh_remote()

    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)

        # 分割器
        splitter = QSplitter(Qt.Horizontal)

        # 本地文件面板
        local_panel = self._create_panel("本地文件", is_remote=False)
        splitter.addWidget(local_panel)

        # 远程文件面板
        remote_panel = self._create_panel("远程文件", is_remote=True)
        splitter.addWidget(remote_panel)

        splitter.setSizes([400, 400])
        layout.addWidget(splitter)

        # 传输进度
        progress_layout = QHBoxLayout()
        self.progress_label = QLabel("就绪")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        layout.addLayout(progress_layout)

    def _create_panel(self, title: str, is_remote: bool) -> QWidget:
        """创建文件面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # 标题和路径
        header_layout = QHBoxLayout()
        title_label = QLabel(title)
        header_layout.addWidget(title_label)

        path_label = QLabel()
        path_label.setStyleSheet("color: gray;")
        header_layout.addWidget(path_label, 1)

        if is_remote:
            self.remote_path_label = path_label
        else:
            self.local_path_label = path_label

        layout.addLayout(header_layout)

        # 文件列表
        file_list = FileListWidget(is_remote=is_remote)
        file_list.file_double_clicked.connect(
            lambda name, is_dir: self._on_file_double_clicked(name, is_dir, is_remote)
        )
        layout.addWidget(file_list)

        if is_remote:
            self.remote_list = file_list
        else:
            self.local_list = file_list

        # 操作按钮
        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(
            lambda: self._refresh_remote() if is_remote else self._refresh_local()
        )
        button_layout.addWidget(refresh_btn)

        if is_remote:
            download_btn = QPushButton("下载")
            download_btn.clicked.connect(self._download_file)
            button_layout.addWidget(download_btn)

            mkdir_btn = QPushButton("新建文件夹")
            mkdir_btn.clicked.connect(self._mkdir_remote)
            button_layout.addWidget(mkdir_btn)
        else:
            upload_btn = QPushButton("上传")
            upload_btn.clicked.connect(self._upload_file)
            button_layout.addWidget(upload_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        return panel

    def set_sftp_client(self, sftp_client: SFTPClient):
        """设置SFTP客户端"""
        self.sftp_client = sftp_client
        self._refresh_remote()

    def _refresh_local(self):
        """刷新本地文件列表"""
        try:
            path = self.local_list.current_path
            files = os.listdir(path)
            files = [f for f in files if not f.startswith('.')]
            files.sort(key=lambda f: (not os.path.isdir(os.path.join(path, f)), f.lower()))

            self.local_list.set_files(files)
            self.local_path_label.setText(path)

        except Exception as e:
            QMessageBox.warning(self, "错误", f"读取本地目录失败: {e}")

    def _refresh_remote(self):
        """刷新远程文件列表"""
        if not self.sftp_client:
            return

        try:
            path = self.remote_list.current_path
            files = self.sftp_client.list_dir(path)
            self.remote_list.set_files(files)
            self.remote_path_label.setText(path)

        except Exception as e:
            QMessageBox.warning(self, "错误", f"读取远程目录失败: {e}")

    def _on_file_double_clicked(self, filename: str, is_dir: bool, is_remote: bool):
        """文件双击事件"""
        if not is_dir:
            return

        if is_remote:
            current_path = self.remote_list.current_path
            if filename == "..":
                new_path = os.path.dirname(current_path.rstrip('/'))
                if not new_path:
                    new_path = "/"
            else:
                new_path = os.path.join(current_path, filename)

            self.remote_list.current_path = new_path
            self._refresh_remote()
        else:
            current_path = self.local_list.current_path
            if filename == "..":
                new_path = os.path.dirname(current_path)
            else:
                new_path = os.path.join(current_path, filename)

            if os.path.exists(new_path):
                self.local_list.current_path = new_path
                self._refresh_local()

    def _upload_file(self):
        """上传文件"""
        if not self.sftp_client:
            QMessageBox.warning(self, "错误", "未连接到远程服务器")
            return

        filename, is_dir = self.local_list.get_selected_file()
        if not filename or filename == "..":
            QMessageBox.warning(self, "提示", "请选择要上传的文件")
            return

        if is_dir:
            QMessageBox.warning(self, "提示", "暂不支持上传文件夹")
            return

        local_path = os.path.join(self.local_list.current_path, filename)
        remote_path = os.path.join(self.remote_list.current_path, filename).replace('\\', '/')

        self._start_transfer("upload", local_path, remote_path)

    def _download_file(self):
        """下载文件"""
        if not self.sftp_client:
            QMessageBox.warning(self, "错误", "未连接到远程服务器")
            return

        filename, is_dir = self.remote_list.get_selected_file()
        if not filename or filename == "..":
            QMessageBox.warning(self, "提示", "请选择要下载的文件")
            return

        if is_dir:
            QMessageBox.warning(self, "提示", "暂不支持下载文件夹")
            return

        remote_path = os.path.join(self.remote_list.current_path, filename).replace('\\', '/')
        local_path = os.path.join(self.local_list.current_path, filename)

        self._start_transfer("download", local_path, remote_path)

    def _start_transfer(self, operation: str, local_path: str, remote_path: str):
        """开始文件传输"""
        if self.transfer_thread and self.transfer_thread.isRunning():
            QMessageBox.warning(self, "提示", "有文件正在传输中")
            return

        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.progress_label.setText(f"{'上传' if operation == 'upload' else '下载'}中...")

        self.transfer_thread = FileTransferThread(
            operation, self.sftp_client, local_path, remote_path
        )
        self.transfer_thread.progress.connect(self._on_transfer_progress)
        self.transfer_thread.finished.connect(self._on_transfer_finished)
        self.transfer_thread.start()

    def _on_transfer_progress(self, progress: int):
        """传输进度更新"""
        self.progress_bar.setValue(progress)

    def _on_transfer_finished(self, success: bool, message: str):
        """传输完成"""
        self.progress_bar.setVisible(False)
        self.progress_label.setText("就绪")

        if success:
            QMessageBox.information(self, "成功", message)
            self._refresh_local()
            self._refresh_remote()
        else:
            QMessageBox.warning(self, "失败", message)

    def _mkdir_remote(self):
        """创建远程目录"""
        if not self.sftp_client:
            QMessageBox.warning(self, "错误", "未连接到远程服务器")
            return

        dirname, ok = QInputDialog.getText(self, "新建文件夹", "文件夹名称:")
        if ok and dirname:
            remote_path = os.path.join(self.remote_list.current_path, dirname).replace('\\', '/')
            if self.sftp_client.mkdir(remote_path):
                QMessageBox.information(self, "成功", "文件夹创建成功")
                self._refresh_remote()
            else:
                QMessageBox.warning(self, "失败", "文件夹创建失败")

    def closeEvent(self, event):
        """关闭事件"""
        if self.transfer_thread and self.transfer_thread.isRunning():
            reply = QMessageBox.question(
                self, "确认", "有文件正在传输，确定要关闭吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return

            self.transfer_thread.terminate()
            self.transfer_thread.wait()

        event.accept()
