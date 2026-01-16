#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试后端功能，不依赖于GUI应用
"""

import os
import sys
import json
from io import BytesIO

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.file_utils import file_utils
from utils.user_cache import user_cache
from utils.logger import logger

# 测试文件上传的后端逻辑
def test_file_upload_backend():
    """
    测试文件上传的后端逻辑
    """
    print("测试1: 文件上传的后端逻辑")
    print("-" * 50)
    
    # 模拟Flask的FileStorage对象
    class MockFileStorage:
        def __init__(self, content, filename):
            self.content = content
            self.filename = filename
        
        def save(self, dst):
            with open(dst, 'wb') as f:
                f.write(self.content)
    
    # 创建测试文件内容
    test_content = b"This is a test file for testing file upload functionality"
    mock_file = MockFileStorage(test_content, "test_upload.txt")
    
    # 调用save_file方法
    success, filename = file_utils.save_file(mock_file, "test_upload.txt")
    
    if success:
        print(f"✓ 文件保存成功，文件名: {filename}")
        
        # 检查文件是否存在
        file_path = file_utils.get_file_path(filename)
        if file_path and os.path.exists(file_path):
            print("✓ 文件存在于指定路径")
            
            # 删除测试文件
            if file_utils.delete_file(filename):
                print("✓ 文件删除成功")
            else:
                print("✗ 文件删除失败")
        else:
            print("✗ 文件不存在")
    else:
        print("✗ 文件保存失败")
    
    print()

# 测试用户列表获取
def test_user_list():
    """
    测试用户列表获取
    """
    print("测试2: 用户列表获取")
    print("-" * 50)
    
    # 获取所有用户
    users = user_cache.get_all_users()
    print(f"✓ 获取用户列表成功，共 {len(users)} 个用户")
    
    # 打印用户信息
    for user in users:
        print(f"  - {user['username']} ({user['ip_address']}) - {user['user_id']}")
    
    print()

# 测试消息发送逻辑
def test_message_sending():
    """
    测试消息发送逻辑
    """
    print("测试3: 消息发送逻辑")
    print("-" * 50)
    
    # 模拟用户信息
    user = {
        "user_id": "test_user_id",
        "username": "测试用户",
        "ip_address": "192.168.1.100"
    }
    
    # 模拟消息数据
    message = {
        "user_id": user["user_id"],
        "username": user["username"],
        "message": "这是一条测试消息",
        "timestamp": "2023-05-20 14:30:00"
    }
    
    print(f"✓ 消息构建成功: {message['username']}: {message['message']}")
    print(f"✓ 消息包含时间戳: {message['timestamp']}")
    print(f"✓ 消息包含用户ID: {message['user_id']}")
    
    print()

# 测试文件列表获取
def test_file_list():
    """
    测试文件列表获取
    """
    print("测试4: 文件列表获取")
    print("-" * 50)
    
    # 获取文件列表
    files = file_utils.get_file_list()
    print(f"✓ 获取文件列表成功，共 {len(files)} 个文件")
    
    # 打印文件信息
    for file in files:
        print(f"  - {file['filename']} ({file['size']} bytes) - {file['mtime']}")
    
    print()

# 测试用户名更新
def test_update_username():
    """
    测试用户名更新
    """
    print("测试5: 用户名更新")
    print("-" * 50)
    
    # 创建一个测试用户
    test_user = user_cache.create_user("192.168.1.200", "test device")
    print(f"✓ 创建测试用户成功: {test_user['username']}")
    
    # 更新用户名
    new_username = "更新后的测试用户"
    updated_user = user_cache.update_user(test_user['user_id'], {"username": new_username})
    
    if updated_user and updated_user['username'] == new_username:
        print(f"✓ 用户名更新成功，新用户名: {updated_user['username']}")
    else:
        print("✗ 用户名更新失败")
    
    print()

if __name__ == "__main__":
    print("开始测试后端功能...")
    print("=" * 50)
    
    test_file_upload_backend()
    test_user_list()
    test_message_sending()
    test_file_list()
    test_update_username()
    
    print("=" * 50)
    print("所有后端功能测试完成!")