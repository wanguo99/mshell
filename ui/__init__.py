"""UI模块

包含连接配置对话框和其他UI组件。
"""

from .connection_dialogs import (
    SSHConnectionDialog,
    SerialConnectionDialog,
    SavedConnectionsDialog
)

__all__ = [
    'SSHConnectionDialog',
    'SerialConnectionDialog',
    'SavedConnectionsDialog',
]
