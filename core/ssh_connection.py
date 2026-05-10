"""SSH连接管理

基于paramiko实现SSH连接，支持密码和密钥认证。
"""

import threading
import time
from typing import Optional

import paramiko

from core.connection_manager import ConnectionManager


class SSHConnection(ConnectionManager):
    """SSH连接管理器"""

    def __init__(self):
        super().__init__()
        self._client: Optional[paramiko.SSHClient] = None
        self._channel: Optional[paramiko.Channel] = None
        self._receive_thread: Optional[threading.Thread] = None
        self._running = False

    def connect(self, host: str, port: int = 22, username: str = "",
                password: str = "", key_file: str = "", timeout: int = 10) -> bool:
        """建立SSH连接

        Args:
            host: 主机地址
            port: 端口号
            username: 用户名
            password: 密码（密码认证）
            key_file: 密钥文件路径（密钥认证）
            timeout: 连接超时时间（秒）

        Returns:
            连接是否成功
        """
        try:
            # 创建SSH客户端
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 连接参数
            connect_kwargs = {
                'hostname': host,
                'port': port,
                'username': username,
                'timeout': timeout,
            }

            # 选择认证方式
            if key_file:
                # 密钥认证
                try:
                    key = paramiko.RSAKey.from_private_key_file(key_file)
                    connect_kwargs['pkey'] = key
                except Exception:
                    # 尝试其他密钥类型
                    try:
                        key = paramiko.Ed25519Key.from_private_key_file(key_file)
                        connect_kwargs['pkey'] = key
                    except Exception:
                        key = paramiko.ECDSAKey.from_private_key_file(key_file)
                        connect_kwargs['pkey'] = key
            else:
                # 密码认证
                connect_kwargs['password'] = password

            # 建立连接
            self._client.connect(**connect_kwargs)

            # 创建交互式shell
            self._channel = self._client.invoke_shell(
                term='xterm-256color',
                width=80,
                height=24
            )

            # 设置为非阻塞模式
            self._channel.setblocking(False)

            # 启动接收线程
            self._running = True
            self._receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self._receive_thread.start()

            # 通知连接成功
            self._notify_connection_changed(True)

            return True

        except Exception as e:
            print(f"SSH connection failed: {e}")
            self._cleanup()
            return False

    def disconnect(self):
        """断开SSH连接"""
        self._running = False

        # 等待接收线程结束
        if self._receive_thread and self._receive_thread.is_alive():
            self._receive_thread.join(timeout=2)

        # 清理资源
        self._cleanup()

        # 通知连接断开
        self._notify_connection_changed(False)

    def send(self, data: bytes):
        """发送数据到SSH服务器

        Args:
            data: 要发送的字节数据
        """
        if not self.is_connected():
            return

        try:
            self._channel.send(data)
        except Exception as e:
            print(f"SSH send failed: {e}")
            self.disconnect()

    def is_connected(self) -> bool:
        """检查SSH是否已连接

        Returns:
            是否已连接
        """
        return (self._client is not None and
                self._channel is not None and
                self._channel.get_transport() is not None and
                self._channel.get_transport().is_active())

    def _receive_loop(self):
        """接收数据循环（在独立线程中运行）"""
        while self._running and self.is_connected():
            try:
                if self._channel.recv_ready():
                    data = self._channel.recv(4096)
                    if data:
                        self._notify_data_received(data)
                    else:
                        # 连接关闭
                        break
                else:
                    # 短暂休眠避免CPU占用过高
                    time.sleep(0.01)

            except Exception as e:
                print(f"SSH receive error: {e}")
                break

        # 接收循环结束，断开连接
        if self._running:
            self.disconnect()

    def _cleanup(self):
        """清理资源"""
        if self._channel:
            try:
                self._channel.close()
            except Exception:
                pass
            self._channel = None

        if self._client:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None

    def resize_terminal(self, width: int, height: int):
        """调整终端大小

        Args:
            width: 终端宽度（字符数）
            height: 终端高度（行数）
        """
        if self._channel:
            try:
                self._channel.resize_pty(width=width, height=height)
            except Exception as e:
                print(f"Resize terminal failed: {e}")
