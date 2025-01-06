# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:07:04 2025

@author: Ting
"""

# 导入所需的模块和功能
import re  # 正则表达式模块
from nltk.corpus import stopwords  # NLTK的停用词模块
from nltk.tokenize import word_tokenize  # NLTK的分词模块
from collections import Counter  # 用于计数的模块
import matplotlib.pyplot as plt  # 绘图模块

# 定义文件路径
file_path = 'D:/A 自然语言处理/存储文件/dh/练习文档/2024-12-12 CFA Institute eyes growing demand for ESG talent in China.txt'

# 使用with语句打开文件，确保文件会被正确关闭
with open(file_path, 'r', encoding='utf-8') as file:
    # 读取文件内容并赋值给变量s
    s = file.read()

# 指定停用词
cache_english_stopwords = stopwords.words('english')

# 定义一个函数来清洗文本
def text_clean(text):
    # 将换行符替换为空格，以避免分词时出现空白
    text = text.replace('\n', ' ')
    
    # 去除所有非数字、字母和单引号（如I'm中的'）的字符
    text_no_special_entities = re.sub(r'[^a-zA-Z0-9\'\ ]', '', text)
    
    # 去除所有的's
    text_no_possessive_case = re.sub(r'\'s','',text_no_special_entities)
    
    # 去除多余的空格，只保留一个空格分隔单词
    text_no_whitespace = re.sub(r'\s{2,}', ' ', text_no_possessive_case)
    
    # 使用NLTK的word_tokenize函数进行分词
    tokens = word_tokenize(text_no_whitespace)
    
    # 将所有单词变为小写，以避免大小写差异导致的重复
    tokens = [word.lower() for word in tokens]
    
    # 去除停用词
    list_no_stopwords = [word for word in tokens if word not in cache_english_stopwords]
    
    # 将清洗后的单词列表连接成一个字符串，以空格分隔
    text_filtered = ' '.join(list_no_stopwords)
    
    # 返回清洗后的文本
    return text_filtered

# 调用text_clean函数清洗文本
cleaned_text = text_clean(s)

# 计算清洗后的文本中每个单词的频率
word_freq = Counter(cleaned_text.split())  # 使用split()将字符串分割成单词列表

# 使用matplotlib绘制词频图表
plt.figure(figsize=(50, 20))  # 设置图表大小
# 绘制前10个最常见单词的折线图，确保x轴是单词，y轴是频率
words = [word for word, count in word_freq.most_common(10)]
counts = [count for word, count in word_freq.most_common(10)]
plt.plot(words, counts, marker='o')  # 使用'o'标记每个数据点
plt.xlabel('Words')  # 设置x轴标签
plt.ylabel('Frequency')  # 设置y轴标签
plt.title('Word Frequency')  # 设置图表标题
plt.xticks(rotation=90)  # 将x轴标签旋转90度，以便更好地显示
plt.show()  # 显示图表

import pandas as pd

# 创建一个DataFrame
df = pd.DataFrame(word_freq.most_common(10), columns=['Word', 'Frequency'])

# 指定保存路径，例如保存到桌面上的一个名为"Reports"的文件夹中
save_path = 'D:/A 自然语言处理/存储文件/dh/excel/word_freq.xlsx'

# 将DataFrame保存为Excel文件到指定路径
df.to_excel(save_path, index=False)





