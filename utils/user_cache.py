import json
import os
import uuid
from datetime import datetime
from .logger import logger

class UserCache:
    """
    用户缓存管理类，用于处理用户信息的存储和读取
    """
    
    def __init__(self, cache_file="users.json"):
        """
        初始化用户缓存
        
        Args:
            cache_file: 用户缓存文件路径
        """
        self.cache_file = cache_file
        self.users = self._load_users()
        # 在线用户字典，key为user_id，value为连接计数
        self.online_users = {}
        # 用户ID到socket_id列表的映射，用于跟踪每个用户的所有连接
        self.user_connections = {}
    
    def _load_users(self):
        """
        从文件加载用户数据
        
        Returns:
            list: 用户列表
        """
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("users", [])
            return []
        except Exception as e:
            logger.error(f"加载用户缓存失败: {e}")
            return []
    
    def _save_users(self):
        """
        保存用户数据到文件
        """
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump({"users": self.users}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存用户缓存失败: {e}")
    
    def get_user_by_ip(self, ip_address):
        """
        根据IP地址获取用户信息
        
        Args:
            ip_address: 用户IP地址
        
        Returns:
            dict or None: 用户信息或None
        """
        for user in self.users:
            if user.get("ip_address") == ip_address:
                return user
        return None
    
    def create_user(self, ip_address, device_info=""):
        """
        创建新用户
        
        Args:
            ip_address: 用户IP地址
            device_info: 设备信息
        
        Returns:
            dict: 新用户信息
        """
        # 检查是否已有该IP的用户
        existing_user = self.get_user_by_ip(ip_address)
        if existing_user:
            return existing_user
        
        # 创建新用户
        user_id = str(uuid.uuid4())
        username = f"用户_{len(self.users) + 1}"
        user = {
            "user_id": user_id,
            "username": username,
            "ip_address": ip_address,
            "device_info": device_info,
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 添加到用户列表并保存
        self.users.append(user)
        self._save_users()
        logger.info(f"创建新用户: {username} ({ip_address})")
        return user
    
    def update_user(self, user_id, update_data):
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            update_data: 要更新的数据
        
        Returns:
            dict or None: 更新后的用户信息或None
        """
        for i, user in enumerate(self.users):
            if user.get("user_id") == user_id:
                self.users[i].update(update_data)
                self.users[i]["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_users()
                logger.info(f"更新用户信息: {user.get('username')} -> {update_data}")
                return self.users[i]
        return None
    
    def get_all_users(self):
        """
        获取所有用户
        
        Returns:
            list: 用户列表
        """
        return self.users
    
    def update_user_last_seen(self, user_id):
        """
        更新用户最后在线时间
        
        Args:
            user_id: 用户ID
        """
        self.update_user(user_id, {})
    
    def add_online_user(self, user_id, socket_id=None):
        """
        添加在线用户
        
        Args:
            user_id: 用户ID
            socket_id: 可选，socket连接ID，用于跟踪用户的连接
        """
        # 更新在线用户计数
        if user_id in self.online_users:
            self.online_users[user_id] += 1
        else:
            self.online_users[user_id] = 1
        
        # 记录socket_id到user_id的映射
        if socket_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(socket_id)
    
    def remove_online_user(self, user_id, socket_id=None):
        """
        移除在线用户
        
        Args:
            user_id: 用户ID
            socket_id: 可选，socket连接ID，用于移除特定连接
        """
        # 更新连接计数
        if user_id in self.online_users:
            self.online_users[user_id] -= 1
            # 如果计数为0，从在线用户字典中移除
            if self.online_users[user_id] <= 0:
                del self.online_users[user_id]
        
        # 更新socket连接映射
        if socket_id and user_id in self.user_connections:
            self.user_connections[user_id].discard(socket_id)
            # 如果用户没有连接了，移除该用户的连接映射
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
    
    def get_user_by_socket_id(self, socket_id):
        """
        根据socket_id获取用户ID
        
        Args:
            socket_id: socket连接ID
        
        Returns:
            str or None: 用户ID或None
        """
        for user_id, sockets in self.user_connections.items():
            if socket_id in sockets:
                return user_id
        return None
    
    def get_online_users(self):
        """
        获取在线用户列表
        
        Returns:
            list: 在线用户列表
        """
        online_user_list = []
        for user in self.users:
            if user.get('user_id') in self.online_users:
                online_user_list.append(user)
        return online_user_list

# 创建全局用户缓存实例
user_cache = UserCache()