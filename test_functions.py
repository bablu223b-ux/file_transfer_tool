#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本，用于验证各个模块的功能
"""

import os
import sys
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.file_utils import file_utils
from utils.user_cache import user_cache
from utils.logger import logger

print("开始测试各个模块的功能...")

# 测试文件工具类
print("\n1. 测试文件工具类:")
try:
    # 测试获取文件列表
    files = file_utils.get_file_list()
    print(f"   - 获取文件列表成功，共 {len(files)} 个文件")
    
    # 测试创建临时文件并保存
    from io import BytesIO
    test_file = BytesIO(b"test content")
    success, filename = file_utils.save_file(test_file, "test.txt")
    if success:
        print(f"   - 文件保存成功，文件名: {filename}")
        
        # 测试获取文件路径
        file_path = file_utils.get_file_path(filename)
        if file_path and os.path.exists(file_path):
            print("   - 获取文件路径成功")
        else:
            print("   - 获取文件路径失败")
        
        # 测试删除文件
        if file_utils.delete_file(filename):
            print("   - 文件删除成功")
        else:
            print("   - 文件删除失败")
    else:
        print("   - 文件保存失败")
except Exception as e:
    print(f"   - 测试失败: {e}")

# 测试用户缓存类
print("\n2. 测试用户缓存类:")
try:
    # 测试创建用户
    user = user_cache.create_user("192.168.1.100", "test device")
    print(f"   - 创建用户成功，用户名: {user['username']}")
    
    # 测试根据IP获取用户
    user_by_ip = user_cache.get_user_by_ip("192.168.1.100")
    if user_by_ip:
        print(f"   - 根据IP获取用户成功，用户名: {user_by_ip['username']}")
    else:
        print("   - 根据IP获取用户失败")
    
    # 测试更新用户名
    updated_user = user_cache.update_user(user['user_id'], {"username": "测试用户"})
    if updated_user and updated_user['username'] == "测试用户":
        print("   - 更新用户名成功")
    else:
        print("   - 更新用户名失败")
    
    # 测试获取所有用户
    all_users = user_cache.get_all_users()
    print(f"   - 获取所有用户成功，共 {len(all_users)} 个用户")
    
    # 测试更新用户最后在线时间
    user_cache.update_user_last_seen(user['user_id'])
    print("   - 更新用户最后在线时间成功")
except Exception as e:
    print(f"   - 测试失败: {e}")

# 测试配置文件
print("\n3. 测试配置文件:")
try:
    with open("config.json", "r") as f:
        config = json.load(f)
    print(f"   - 加载配置文件成功，服务器端口: {config['server_port']}")
except Exception as e:
    print(f"   - 测试失败: {e}")

print("\n所有测试完成!")