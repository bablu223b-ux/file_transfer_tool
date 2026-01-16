#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复的功能是否正常工作
"""

import requests
import json
import time
import os

# 测试服务器URL
SERVER_URL = "http://localhost:5000"

def test_server_running():
    """
    测试服务器是否正在运行
    """
    print("测试1: 检查服务器是否正在运行...")
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            print("   ✓ 服务器正在运行")
            return True
        else:
            print(f"   ✗ 服务器返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ 服务器未运行: {e}")
        return False

def test_get_users():
    """
    测试获取用户列表API
    """
    print("测试2: 测试获取用户列表API...")
    try:
        response = requests.get(f"{SERVER_URL}/api/users")
        if response.status_code == 200:
            data = response.json()
            if "users" in data:
                print(f"   ✓ 获取用户列表成功，共 {len(data['users'])} 个用户")
                return True
            else:
                print("   ✗ 返回数据格式错误")
                return False
        else:
            print(f"   ✗ 请求失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ 请求失败: {e}")
        return False

def test_get_files():
    """
    测试获取文件列表API
    """
    print("测试3: 测试获取文件列表API...")
    try:
        response = requests.get(f"{SERVER_URL}/api/files")
        if response.status_code == 200:
            data = response.json()
            if "files" in data:
                print(f"   ✓ 获取文件列表成功，共 {len(data['files'])} 个文件")
                return True
            else:
                print("   ✗ 返回数据格式错误")
                return False
        else:
            print(f"   ✗ 请求失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ 请求失败: {e}")
        return False

def test_file_upload():
    """
    测试文件上传功能
    """
    print("测试4: 测试文件上传功能...")
    try:
        # 创建一个测试文件
        test_file_path = "test_upload.txt"
        with open(test_file_path, "w") as f:
            f.write("这是一个测试文件")
        
        # 上传文件
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f)}
            response = requests.post(f"{SERVER_URL}/upload", files=files)
        
        # 删除测试文件
        os.remove(test_file_path)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"   ✓ 文件上传成功，文件名: {data['filename']}")
                return True
            else:
                print(f"   ✗ 文件上传失败: {data['message']}")
                return False
        else:
            print(f"   ✗ 请求失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ 请求失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试修复的功能...")
    print("=" * 50)
    
    # 测试服务器是否正在运行
    if not test_server_running():
        print("服务器未运行，无法进行后续测试")
        exit(1)
    
    # 测试其他功能
    test_get_users()
    test_get_files()
    test_file_upload()
    
    print("=" * 50)
    print("测试完成!")