"""配置服务，提供统一的配置管理接口"""

from typing import List, Optional
from config.config_manager import ConfigManager
from models.connection import ConnectionConfig, create_connection_config


class ConfigService:
    """配置服务"""

    def __init__(self):
        self._config_manager = ConfigManager()

    def load(self):
        """加载配置"""
        self._config_manager.load()

    def save(self):
        """保存配置"""
        self._config_manager.save()

    def get_connections(self) -> List[ConnectionConfig]:
        """获取所有连接配置

        Returns:
            ConnectionConfig对象列表
        """
        connections_dict = self._config_manager.get_connections()
        return [create_connection_config(conn) for conn in connections_dict]

    def add_connection(self, config: ConnectionConfig) -> bool:
        """添加连接配置

        Args:
            config: 连接配置对象

        Returns:
            是否添加成功
        """
        try:
            connections = self._config_manager.get_connections()

            # 检查是否已存在同名配置
            existing = [c for c in connections if c.get('name') == config.name]
            if existing:
                return False

            # 添加配置（不保存密码）
            save_config = config.config_dict.copy()
            if 'password' in save_config:
                del save_config['password']

            connections.append(save_config)
            self._config_manager.set('connections', connections)
            self._config_manager.save()
            return True

        except Exception as e:
            print(f"添加连接配置失败: {e}")
            return False

    def update_connection(self, config: ConnectionConfig) -> bool:
        """更新连接配置

        Args:
            config: 连接配置对象

        Returns:
            是否更新成功
        """
        try:
            connections = self._config_manager.get_connections()

            # 查找并更新
            for i, conn in enumerate(connections):
                if conn.get('name') == config.name:
                    save_config = config.config_dict.copy()
                    if 'password' in save_config:
                        del save_config['password']
                    connections[i] = save_config
                    self._config_manager.set('connections', connections)
                    self._config_manager.save()
                    return True

            return False

        except Exception as e:
            print(f"更新连接配置失败: {e}")
            return False

    def remove_connection(self, name: str) -> bool:
        """删除连接配置

        Args:
            name: 连接名称

        Returns:
            是否删除成功
        """
        return self._config_manager.remove_connection(name)

    def delete_connection(self, name: str) -> bool:
        """删除连接配置（别名方法）

        Args:
            name: 连接名称

        Returns:
            是否删除成功
        """
        return self.remove_connection(name)

    def get_auto_close_on_disconnect(self) -> Optional[bool]:
        """获取连接断开时自动关闭标签页的配置"""
        return self._config_manager.get('auto_close_on_disconnect')

    def set_auto_close_on_disconnect(self, value: bool):
        """设置连接断开时自动关闭标签页的配置"""
        self._config_manager.set('auto_close_on_disconnect', value)
        self._config_manager.save()

    def get(self, key: str, default=None):
        """获取配置项"""
        return self._config_manager.get(key, default)

    def set(self, key: str, value):
        """设置配置项"""
        self._config_manager.set(key, value)
