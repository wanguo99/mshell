"""快捷指令执行器

执行预定义的快捷指令，支持变量替换。
"""

import re
from typing import Dict, Optional

from core.connection_manager import ConnectionManager


class CommandExecutor:
    """快捷指令执行器"""

    def __init__(self):
        self._variables: Dict[str, str] = {}

    def execute(self, command: str, connection: ConnectionManager,
                variables: Optional[Dict[str, str]] = None):
        """执行快捷指令

        Args:
            command: 指令模板（可包含变量，如 "ssh {user}@{host}"）
            connection: 连接管理器
            variables: 变量字典（如 {"user": "root", "host": "192.168.1.1"}）
        """
        if not connection.is_connected():
            print("Error: Not connected")
            return

        # 合并变量
        all_variables = {**self._variables}
        if variables:
            all_variables.update(variables)

        # 替换变量
        processed_command = self._replace_variables(command, all_variables)

        # 发送指令（添加换行符）
        if not processed_command.endswith('\n'):
            processed_command += '\n'

        try:
            connection.send(processed_command.encode('utf-8'))
        except Exception as e:
            print(f"Execute command failed: {e}")

    def _replace_variables(self, command: str, variables: Dict[str, str]) -> str:
        """替换指令中的变量

        Args:
            command: 指令模板
            variables: 变量字典

        Returns:
            替换后的指令
        """
        # 查找所有 {variable} 格式的变量
        pattern = r'\{(\w+)\}'

        def replace_func(match):
            var_name = match.group(1)
            return variables.get(var_name, match.group(0))

        return re.sub(pattern, replace_func, command)

    def set_variable(self, name: str, value: str):
        """设置全局变量

        Args:
            name: 变量名
            value: 变量值
        """
        self._variables[name] = value

    def get_variable(self, name: str) -> Optional[str]:
        """获取全局变量

        Args:
            name: 变量名

        Returns:
            变量值，不存在则返回None
        """
        return self._variables.get(name)

    def clear_variables(self):
        """清空所有全局变量"""
        self._variables.clear()

    def get_all_variables(self) -> Dict[str, str]:
        """获取所有全局变量

        Returns:
            变量字典
        """
        return self._variables.copy()
