"""异步 SSH 连接适配器

使用 asyncio + paramiko 实现异步 SSH 连接。
注意：paramiko 本身是同步库，这里通过 asyncio.to_thread 包装为异步接口。
"""

import asyncio
import paramiko
from typing import AsyncIterator, Optional
from domain.connection.connection import IConnection


class AsyncSSHAdapter(IConnection):
    """异步 SSH 连接适配器

    将 paramiko 的同步接口包装为异步接口，统一连接抽象。
    """

    def __init__(self):
        self._client: Optional[paramiko.SSHClient] = None
        self._channel: Optional[paramiko.Channel] = None
        self._running = False
        self._receive_task: Optional[asyncio.Task] = None

    @property
    def connection_type(self) -> str:
        return 'ssh'

    async def connect(self, host: str, port: int = 22, username: str = "",
                     password: str = "", key_file: str = "", timeout: int = 10) -> bool:
        """异步建立 SSH 连接

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
            # 在线程池中执行同步连接操作
            await asyncio.to_thread(self._connect_sync, host, port, username,
                                   password, key_file, timeout)
            self._running = True
            return True

        except Exception as e:
            print(f"SSH connection failed: {e}")
            await self._cleanup()
            return False

    def _connect_sync(self, host: str, port: int, username: str,
                     password: str, key_file: str, timeout: int) -> None:
        """同步连接（在线程池中执行）"""
        # 创建 SSH 客户端
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

        # 创建交互式 shell
        self._channel = self._client.invoke_shell(
            term='xterm-256color',
            width=80,
            height=24
        )

        # 设置为非阻塞模式
        self._channel.setblocking(False)

    async def disconnect(self) -> None:
        """异步断开连接"""
        self._running = False

        # 取消接收任务
        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        # 清理资源
        await self._cleanup()

    async def send(self, data: bytes) -> None:
        """异步发送数据

        Args:
            data: 要发送的字节数据
        """
        if not self.is_connected():
            return

        try:
            # 在线程池中执行同步发送
            await asyncio.to_thread(self._channel.send, data)
        except Exception as e:
            print(f"SSH send failed: {e}")
            await self.disconnect()

    async def receive(self) -> AsyncIterator[bytes]:
        """异步接收数据（生成器）

        Yields:
            接收到的字节数据
        """
        while self._running and self.is_connected():
            try:
                # 在线程池中检查是否有数据
                has_data = await asyncio.to_thread(self._channel.recv_ready)

                if has_data:
                    # 在线程池中接收数据
                    data = await asyncio.to_thread(self._channel.recv, 4096)
                    if data:
                        yield data
                    else:
                        # 连接关闭
                        break
                else:
                    # 短暂休眠避免 CPU 占用过高
                    await asyncio.sleep(0.01)

            except Exception as e:
                print(f"SSH receive error: {e}")
                break

        # 接收循环结束，断开连接
        if self._running:
            await self.disconnect()

    def is_connected(self) -> bool:
        """检查 SSH 是否已连接

        Returns:
            是否已连接
        """
        return (self._client is not None and
                self._channel is not None and
                self._channel.get_transport() is not None and
                self._channel.get_transport().is_active())

    async def resize_terminal(self, rows: int, cols: int) -> None:
        """调整终端大小

        Args:
            rows: 终端行数
            cols: 终端列数
        """
        if self._channel:
            try:
                await asyncio.to_thread(self._channel.resize_pty, width=cols, height=rows)
            except Exception as e:
                print(f"Resize terminal failed: {e}")

    async def _cleanup(self) -> None:
        """清理资源"""
        if self._channel:
            try:
                await asyncio.to_thread(self._channel.close)
            except Exception:
                pass
            self._channel = None

        if self._client:
            try:
                await asyncio.to_thread(self._client.close)
            except Exception:
                pass
            self._client = None
