# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 18:06:36 2025

@author: Ting
"""

import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd


# 定义文件夹路径
folder_path = 'D:/A 自然语言处理/存储文件/dh/2024-12'


# 获取文件夹内所有txt文件
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]


# 指定保存Excel文件的文件夹路径
excel_folder_path = 'D:/A 自然语言处理/存储文件/dh/excel'


# 指定保存折线图的文件夹路径
plot_folder_path = 'D:/A 自然语言处理/存储文件/dh/折线图'


# 如果Excel文件夹不存在，则创建
if not os.path.exists(excel_folder_path):
    os.makedirs(excel_folder_path)


# 如果折线图文件夹不存在，则创建
if not os.path.exists(plot_folder_path):
    os.makedirs(plot_folder_path)


# 指定停用词
cache_english_stopwords = stopwords.words('english')


# 定义一个函数来清洗文本
def text_clean(text):
    text = text.replace('\n', ' ')
    text_no_special_entities = re.sub(r'[^a-zA-Z\'\ ]', '', text)
    text_no_possessive_case = re.sub(r'\'s|\'', '', text_no_special_entities)
    text_no_whitespace = re.sub(r'\s{2,}', ' ', text_no_possessive_case)
    tokens = word_tokenize(text_no_whitespace)
    tokens = [word.lower() for word in tokens]
    list_no_stopwords = [word for word in tokens if word not in cache_english_stopwords]
    text_filtered = ' '.join(list_no_stopwords)
    return text_filtered


# 遍历所有txt文件
for txt_file in txt_files:
    # 如果文件名是all_titles.txt则跳过，不进行后续处理，以此达到不生成对应文件的目的
    if txt_file == "all_titles.txt":
        continue
    # 定义文件路径
    file_path = os.path.join(folder_path, txt_file)
    
    # 读取文件内容，跳过第一行（标题）
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        body_text = ''.join(lines[1:])  # 跳过第一行，合并剩余的正文内容
    
    # 清洗正文文本
    cleaned_text = text_clean(body_text)
    
    # 初始化词频统计器
    word_freq = Counter()
    
    # 计算清洗后的正文文本中每个单词的频率
    word_freq.update(cleaned_text.split())
    
    # 创建一个DataFrame
    df = pd.DataFrame(word_freq.most_common(10), columns=['Word', 'Frequency'])
    
    # 定义Excel文件名，与txt文件名对应
    excel_file_name = os.path.splitext(txt_file)[0] + '.xlsx'
    save_path_excel = os.path.join(excel_folder_path, excel_file_name)
    
    # 将DataFrame保存为Excel文件到指定路径
    df.to_excel(save_path_excel, index=False)
    
    # 绘制前10个最常见单词的折线图
    words = [word for word, count in word_freq.most_common(10)]
    counts = [count for word, count in word_freq.most_common(10)]
    plt.figure(figsize=(12, 6))  # 调整图表大小
    plt.plot(words, counts, marker='o')
    plt.xlabel('Words', fontsize=12)  # 调整字体大小
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Word Frequency for ' + txt_file, fontsize=14)
    plt.xticks(rotation=45, fontsize=10)  # 调整标签旋转角度和字体大小
    
    # 定义折线图文件名，与txt文件名对应
    plot_file_name = os.path.splitext(txt_file)[0] + '.png'
    save_path_plot = os.path.join(plot_folder_path, plot_file_name)
    
    # 保存折线图到指定路径
    plt.savefig(save_path_plot, bbox_inches='tight')  # 保存图表，调整边界以适应标签
    plt.close()  # 关闭图表，避免显示在屏幕上
    
    print(f'Saved {excel_file_name} to {excel_folder_path}')
    print(f'Saved {plot_file_name} to {plot_folder_path}')