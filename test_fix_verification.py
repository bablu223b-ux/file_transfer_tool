#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的功能是否正常工作
"""

import requests
import socketio
import time
import os

# 测试服务器URL
SERVER_URL = "http://localhost:5000"
SOCKET_URL = "http://localhost:5000"

def test_file_upload():
    """
    测试文件上传功能
    """
    print("测试1: 文件上传功能")
    print("-" * 50)
    
    try:
        # 创建一个测试文件
        test_file_path = "test_upload.txt"
        with open(test_file_path, "w") as f:
            f.write("这是一个测试文件，用于测试文件上传功能")
        
        # 上传文件
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f)}
            response = requests.post(f"{SERVER_URL}/upload", files=files)
        
        # 删除测试文件
        os.remove(test_file_path)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✓ 文件上传成功，文件名: {data['filename']}")
                return True
            else:
                print(f"✗ 文件上传失败: {data['message']}")
                return False
        else:
            print(f"✗ 请求失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False

def test_socket_connection():
    """
    测试Socket连接和事件处理
    """
    print("测试2: Socket连接和事件处理")
    print("-" * 50)
    
    try:
        # 创建SocketIO客户端
        sio = socketio.Client()
        
        # 事件处理函数
        def on_connect():
            print("✓ Socket连接成功")
            
        def on_disconnect():
            print("✗ Socket断开连接")
            
        def on_login_success(user):
            print(f"✓ 登录成功，用户名: {user['username']}")
            
        def on_user_list_update(data):
            print(f"✓ 用户列表更新，共 {len(data['users'])} 个用户")
            for user in data['users']:
                print(f"  - {user['username']} ({user['ip_address']})")
            
        def on_file_list_update(data):
            print(f"✓ 文件列表更新，共 {len(data['files'])} 个文件")
            
        def on_new_message(message):
            print(f"✓ 收到消息: {message['username']}: {message['message']}")
        
        # 注册事件处理函数
        sio.on('connect', on_connect)
        sio.on('disconnect', on_disconnect)
        sio.on('login_success', on_login_success)
        sio.on('user_list_update', on_user_list_update)
        sio.on('file_list_update', on_file_list_update)
        sio.on('new_message', on_new_message)
        
        # 连接到服务器
        sio.connect(SOCKET_URL)
        
        # 发送登录事件
        sio.emit('user_login', {
            'device_info': 'test device'
        })
        
        # 等待一段时间，让事件处理完成
        time.sleep(2)
        
        # 发送一条消息
        sio.emit('send_message', {
            'message': '这是一条测试消息'
        })
        
        # 等待一段时间，让消息发送完成
        time.sleep(1)
        
        # 断开连接
        sio.disconnect()
        
        print("✓ Socket测试完成")
        return True
    except Exception as e:
        print(f"✗ Socket测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试修复后的功能...")
    print("=" * 50)
    
    # 先等待一会儿，确保服务器已经启动
    time.sleep(3)
    
    # 测试文件上传
    test_file_upload()
    
    # 测试Socket连接和事件处理
    test_socket_connection()
    
    print("=" * 50)
    print("所有测试完成!")