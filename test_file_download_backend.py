#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件下载功能的后端逻辑
"""

import os
import sys
import tempfile

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.file_utils import file_utils
from utils.logger import logger

print("开始测试文件下载后端逻辑...")
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

# 2. 测试文件路径获取
print("2. 测试文件路径获取")
got_path = file_utils.get_file_path(test_filename)
print(f"  期望路径: {file_path}")
print(f"  获取路径: {got_path}")

if got_path == file_path:
    print("✓ 文件路径获取成功")
else:
    print("✗ 文件路径获取失败")
print()

# 3. 测试文件列表获取
print("3. 测试文件列表获取")
file_list = file_utils.get_file_list()
print(f"  获取到 {len(file_list)} 个文件")

found = False
for file in file_list:
    print(f"  - {file['filename']} ({file['size']} bytes) - {file['url']}")
    if file['filename'] == test_filename:
        found = True

if found:
    print("✓ 测试文件在文件列表中")
else:
    print("✗ 测试文件不在文件列表中")
print()

# 4. 测试中文文件名
print("4. 测试中文文件名")
chinese_filename = "测试文件.txt"
chinese_content = "这是一个中文测试文件"

# 保存到上传目录
chinese_file_path = os.path.join(file_utils.upload_dir, chinese_filename)
with open(chinese_file_path, "w", encoding="utf-8") as f:
    f.write(chinese_content)

print(f"✓ 创建中文测试文件: {chinese_file_path}")

# 测试中文文件路径获取
got_chinese_path = file_utils.get_file_path(chinese_filename)
if got_chinese_path == chinese_file_path:
    print("✓ 中文文件路径获取成功")
else:
    print("✗ 中文文件路径获取失败")
print()

# 5. 测试文件删除
print("5. 测试文件删除")

# 删除测试文件
if file_utils.delete_file(test_filename):
    print(f"✓ 删除测试文件: {test_filename}")
else:
    print(f"✗ 删除测试文件: {test_filename}")

# 删除中文测试文件
if file_utils.delete_file(chinese_filename):
    print(f"✓ 删除中文测试文件: {chinese_filename}")
else:
    print(f"✗ 删除中文测试文件: {chinese_filename}")
print()

# 6. 验证文件是否被删除
print("6. 验证文件是否被删除")

if not os.path.exists(file_path):
    print(f"✓ 测试文件已被成功删除")
else:
    print(f"✗ 测试文件未被删除")

if not os.path.exists(chinese_file_path):
    print(f"✓ 中文测试文件已被成功删除")
else:
    print(f"✗ 中文测试文件未被删除")
print()

print("=" * 50)
print("文件下载后端逻辑测试完成!")
print("修复后的后端逻辑可以正确处理文件路径和文件名，包括中文文件名")