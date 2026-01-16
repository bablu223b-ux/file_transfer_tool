#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件下载功能
"""

import os
import sys
import requests
import tempfile

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.file_utils import file_utils
from utils.logger import logger

# 测试服务器URL
SERVER_URL = "http://localhost:5000"

def test_file_download():
    """
    测试文件下载功能
    """
    print("开始测试文件下载功能...")
    print("=" * 50)
    
    # 1. 准备测试文件
    print("1. 准备测试文件")
    test_filename = "test_download.txt"
    test_content = "This is a test file for testing download functionality"
    
    # 保存到上传目录
    file_path = os.path.join(file_utils.upload_dir, test_filename)
    with open(file_path, "w") as f:
        f.write(test_content)
    
    print(f"✓ 创建测试文件: {file_path}")
    print(f"  文件内容: {test_content}")
    print()
    
    # 2. 测试直接访问下载URL
    print("2. 测试直接访问下载URL")
    download_url = f"{SERVER_URL}/download/{test_filename}"
    print(f"  下载URL: {download_url}")
    
    try:
        response = requests.get(download_url)
        if response.status_code == 200:
            print(f"✓ 下载成功，状态码: {response.status_code}")
            print(f"  响应内容: {response.text}")
            
            # 验证内容是否一致
            if response.text == test_content:
                print("✓ 下载的文件内容与原文件一致")
            else:
                print("✗ 下载的文件内容与原文件不一致")
        else:
            print(f"✗ 下载失败，状态码: {response.status_code}")
            print(f"  响应内容: {response.text}")
    except Exception as e:
        print(f"✗ 下载请求失败: {e}")
    
    print()
    
    # 3. 测试中文文件名
    print("3. 测试中文文件名")
    chinese_filename = "测试文件.txt"
    chinese_content = "这是一个中文测试文件"
    
    # 保存到上传目录
    chinese_file_path = os.path.join(file_utils.upload_dir, chinese_filename)
    with open(chinese_file_path, "w", encoding="utf-8") as f:
        f.write(chinese_content)
    
    print(f"✓ 创建中文测试文件: {chinese_file_path}")
    
    # 测试中文文件名下载
    chinese_download_url = f"{SERVER_URL}/download/{chinese_filename}"
    print(f"  中文文件下载URL: {chinese_download_url}")
    
    try:
        response = requests.get(chinese_download_url)
        if response.status_code == 200:
            print(f"✓ 中文文件下载成功，状态码: {response.status_code}")
            print(f"  响应内容: {response.text}")
            
            # 验证内容是否一致
            if response.text == chinese_content:
                print("✓ 下载的中文文件内容与原文件一致")
            else:
                print("✗ 下载的中文文件内容与原文件不一致")
        else:
            print(f"✗ 中文文件下载失败，状态码: {response.status_code}")
            print(f"  响应内容: {response.text}")
    except Exception as e:
        print(f"✗ 中文文件下载请求失败: {e}")
    
    print()
    
    # 4. 清理测试文件
    print("4. 清理测试文件")
    
    # 删除测试文件
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"✓ 删除测试文件: {test_filename}")
    
    if os.path.exists(chinese_file_path):
        os.remove(chinese_file_path)
        print(f"✓ 删除中文测试文件: {chinese_filename}")
    
    print()
    print("=" * 50)
    print("文件下载测试完成!")

if __name__ == "__main__":
    test_file_download()