#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试修复是否有效
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.file_utils import file_utils
from utils.user_cache import user_cache
from utils.logger import logger

print("开始测试修复是否有效...")
print("=" * 50)

# 1. 检查上传目录是否存在
print("测试1: 检查上传目录")
print("-" * 50)
print(f"上传目录: {file_utils.upload_dir}")
if os.path.exists(file_utils.upload_dir):
    print(f"✓ 上传目录存在")
    # 列出目录中的文件
    files = os.listdir(file_utils.upload_dir)
    print(f"  目录中的文件数: {len(files)}")
    for file in files[:5]:  # 只显示前5个文件
        print(f"  - {file}")
    if len(files) > 5:
        print(f"  ... 还有 {len(files) - 5} 个文件")
else:
    print("✗ 上传目录不存在")
print()

# 2. 测试在线用户管理
print("测试2: 在线用户管理")
print("-" * 50)

# 添加测试在线用户
test_user1 = user_cache.create_user("192.168.1.101", "test device 1")
test_user2 = user_cache.create_user("192.168.1.102", "test device 2")

print(f"创建了两个测试用户: {test_user1['username']} 和 {test_user2['username']}")

# 添加到在线用户列表
user_cache.add_online_user(test_user1['user_id'])
user_cache.add_online_user(test_user2['user_id'])

# 获取在线用户列表
online_users = user_cache.get_online_users()
print(f"在线用户列表中有 {len(online_users)} 个用户")
for user in online_users:
    print(f"✓ 在线用户: {user['username']} ({user['ip_address']})")

# 移除一个在线用户
user_cache.remove_online_user(test_user1['user_id'])
online_users = user_cache.get_online_users()
print(f"移除一个用户后，在线用户列表中有 {len(online_users)} 个用户")
for user in online_users:
    print(f"✓ 在线用户: {user['username']} ({user['ip_address']})")

print()

# 3. 测试用户列表更新
print("测试3: 用户列表更新")
print("-" * 50)

# 获取所有用户
all_users = user_cache.get_all_users()
print(f"所有用户列表中有 {len(all_users)} 个用户")
for user in all_users:
    print(f"✓ 用户: {user['username']} ({user['ip_address']}) - 在线: {'是' if user['user_id'] in user_cache.online_users else '否'}")

print()

print("=" * 50)
print("所有测试完成!")