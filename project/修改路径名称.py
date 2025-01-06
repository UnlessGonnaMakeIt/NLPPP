# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 16:58:47 2025

@author: Ting
"""

import os
import shutil

# 定义原始路径和目标路径
source_path = r"C:/Users/Ting/Desktop/数据"
destination_path = r"D:/A NLP/storage/dh/2024-12"

# 确保目标路径存在，如果不存在则创建
os.makedirs(destination_path, exist_ok=True)

# 初始化文件计数器
original_file_count = 0
renamed_file_count = 0

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_path):
    file_path = os.path.join(source_path, filename)

    # 确保处理的对象是文件
    if os.path.isfile(file_path):
        original_file_count += 1
        try:
            # 读取文件的第一行作为新文件名
            with open(file_path, 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()

            # 替换非法字符，避免文件名无效，允许保留空格和部分标点
            valid_name = "".join(c if c.isalnum() or c in " .-_()" else "" for c in first_line).strip()
            if not valid_name:  # 如果第一行内容无效
                valid_name = "Unnamed_File"
            new_filename = valid_name + os.path.splitext(filename)[1]
            new_file_path = os.path.join(destination_path, new_filename)

            # 检查是否已存在同名文件，避免覆盖
            if os.path.exists(new_file_path):
                base, ext = os.path.splitext(new_filename)
                counter = 1
                while os.path.exists(new_file_path):
                    new_file_path = os.path.join(destination_path, f"{base}({counter}){ext}")
                    counter += 1

            # 复制文件到目标文件夹，并以新文件名命名
            shutil.copy(file_path, new_file_path)
            renamed_file_count += 1

            print(f"文件重命名并复制成功: {filename} -> {os.path.basename(new_file_path)}")

        except Exception as e:
            print(f"处理文件时出错: {filename}, 错误: {e}")

# 检查目标路径中的文件是否有命名错误
for renamed_file in os.listdir(destination_path):
    if "__" in renamed_file or renamed_file.startswith("_"):
        print(f"命名可能有问题的文件: {renamed_file}")

# 打印文件计数对比
print(f"原文件夹文件数: {original_file_count}")
print(f"重命名后文件夹文件数: {renamed_file_count}")

print("处理完成！")