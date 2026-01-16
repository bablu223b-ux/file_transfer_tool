#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Socket事件修复是否有效
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.user_cache import user_cache
from utils.logger import logger

print("开始测试Socket事件修复...")
print("=" * 50)

# 创建测试用户
print("1. 创建测试用户")
test_user = user_cache.create_user("192.168.1.103", "test device 3")
print(f"✓ 创建用户: {test_user['username']}")

# 验证用户对象可以被序列化
print("\n2. 验证用户对象可序列化")
try:
    import json
    user_json = json.dumps(test_user)
    print("✓ 用户对象可以被JSON序列化")
    print(f"  序列化结果: {user_json[:50]}...")
except Exception as e:
    print(f"✗ 用户对象无法被JSON序列化: {e}")

# 测试构建发送给前端的用户数据
print("\n3. 测试构建发送给前端的用户数据")
try:
    # 构建前端需要的用户数据
    user_data = {
        "user_id": test_user['user_id'],
        "username": test_user['username'],
        "ip_address": test_user['ip_address'],
        "device_info": test_user.get('device_info', ''),
        "last_seen": test_user.get('last_seen', '')
    }
    
    # 测试序列化
    user_data_json = json.dumps(user_data)
    print("✓ 构建的用户数据可以被JSON序列化")
    print(f"  序列化结果: {user_data_json}")
except Exception as e:
    print(f"✗ 构建的用户数据无法被JSON序列化: {e}")

# 测试在线用户列表构建
print("\n4. 测试在线用户列表构建")
try:
    # 添加到在线用户
    user_cache.add_online_user(test_user['user_id'])
    
    # 获取在线用户列表
    online_users = user_cache.get_online_users()
    print(f"✓ 获取在线用户列表，共 {len(online_users)} 个用户")
    
    # 构建前端需要的在线用户列表
    serialized_users = []
    for u in online_users:
        serialized_users.append({
            "user_id": u['user_id'],
            "username": u['username'],
            "ip_address": u['ip_address'],
            "device_info": u.get('device_info', ''),
            "last_seen": u.get('last_seen', '')
        })
    
    # 测试序列化
    online_users_json = json.dumps(serialized_users)
    print("✓ 构建的在线用户列表可以被JSON序列化")
    print(f"  序列化结果: {online_users_json}")
except Exception as e:
    print(f"✗ 构建在线用户列表失败: {e}")
finally:
    # 清理测试数据
    user_cache.remove_online_user(test_user['user_id'])

print("\n" + "=" * 50)
print("测试完成!")