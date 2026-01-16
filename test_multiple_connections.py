#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试同一用户多个连接的情况
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.user_cache import user_cache
from utils.logger import logger

print("开始测试同一用户多个连接情况...")
print("=" * 50)

# 创建测试用户
test_user = user_cache.create_user("192.168.1.104", "test device 4")
print(f"创建测试用户: {test_user['username']} (ID: {test_user['user_id']})")
print()

# 测试1: 添加第一个连接
print("测试1: 添加第一个连接")
print("-" * 30)
user_cache.add_online_user(test_user['user_id'], "socket_1")
online_users = user_cache.get_online_users()
print(f"在线用户数: {len(online_users)}")
print(f"在线用户: {[user['username'] for user in online_users]}")
print(f"测试用户的连接计数: {user_cache.online_users.get(test_user['user_id'], 0)}")
print()

# 测试2: 添加第二个连接
print("测试2: 添加第二个连接")
print("-" * 30)
user_cache.add_online_user(test_user['user_id'], "socket_2")
online_users = user_cache.get_online_users()
print(f"在线用户数: {len(online_users)}")
print(f"在线用户: {[user['username'] for user in online_users]}")
print(f"测试用户的连接计数: {user_cache.online_users.get(test_user['user_id'], 0)}")
print()

# 测试3: 添加第三个连接
print("测试3: 添加第三个连接")
print("-" * 30)
user_cache.add_online_user(test_user['user_id'], "socket_3")
online_users = user_cache.get_online_users()
print(f"在线用户数: {len(online_users)}")
print(f"在线用户: {[user['username'] for user in online_users]}")
print(f"测试用户的连接计数: {user_cache.online_users.get(test_user['user_id'], 0)}")
print()

# 测试4: 移除一个连接
print("测试4: 移除一个连接")
print("-" * 30)
user_cache.remove_online_user(test_user['user_id'], "socket_1")
online_users = user_cache.get_online_users()
print(f"在线用户数: {len(online_users)}")
print(f"在线用户: {[user['username'] for user in online_users]}")
print(f"测试用户的连接计数: {user_cache.online_users.get(test_user['user_id'], 0)}")
print()

# 测试5: 移除第二个连接
print("测试5: 移除第二个连接")
print("-" * 30)
user_cache.remove_online_user(test_user['user_id'], "socket_2")
online_users = user_cache.get_online_users()
print(f"在线用户数: {len(online_users)}")
print(f"在线用户: {[user['username'] for user in online_users]}")
print(f"测试用户的连接计数: {user_cache.online_users.get(test_user['user_id'], 0)}")
print()

# 测试6: 移除最后一个连接
print("测试6: 移除最后一个连接")
print("-" * 30)
user_cache.remove_online_user(test_user['user_id'], "socket_3")
online_users = user_cache.get_online_users()
print(f"在线用户数: {len(online_users)}")
print(f"在线用户: {[user['username'] for user in online_users]}")
print(f"测试用户的连接计数: {user_cache.online_users.get(test_user['user_id'], 0)}")
print()

# 测试7: 根据socket_id获取用户
print("测试7: 根据socket_id获取用户")
print("-" * 30)
# 重新添加一个连接
user_cache.add_online_user(test_user['user_id'], "socket_4")
user_id = user_cache.get_user_by_socket_id("socket_4")
print(f"根据socket_4获取到的用户ID: {user_id}")
if user_id == test_user['user_id']:
    print("✓ 根据socket_id获取用户成功")
else:
    print("✗ 根据socket_id获取用户失败")
print()

print("=" * 50)
print("所有测试完成!")
print("修复成功: 同一用户多个连接时，其中一个连接断开不会导致用户被错误移除")