# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:37:31 2025

@author: Ting
"""

%matplotlib inline
import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# 定义文件夹路径
folder_path = 'D:/A NLP/storage/dh/2024-12'

# 获取文件夹内所有txt文件
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# 指定保存Excel文件的文件夹路径
excel_folder_path = 'D:/A NLP/storage/dh/excel'

# 指定保存词云图片的文件夹路径
wordcloud_folder_path = 'D:/A NLP/storage/dh/Word Cloud'

# 如果Excel文件夹不存在，则创建
if not os.path.exists(excel_folder_path):
    os.makedirs(excel_folder_path)

# 如果词云文件夹不存在，则创建
if not os.path.exists(wordcloud_folder_path):
    os.makedirs(wordcloud_folder_path)

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

# 初始化汇总文本
all_text = ""

# 遍历所有txt文件
for txt_file in txt_files:
    # 定义文件路径
    file_path = os.path.join(folder_path, txt_file)
    
    # 读取文件内容，跳过第一行（标题）
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        body_text = ''.join(lines[1:])  # 跳过第一行，合并剩余的正文内容
    
    # 将当前文件的正文添加到汇总文本中
    all_text += body_text + " "  # 添加空格以分隔不同文件的内容

# 清洗汇总后的文本
cleaned_text = text_clean(all_text)

# 初始化词频统计器
word_freq = Counter()

# 计算清洗后的汇总文本中每个单词的频率
word_freq.update(cleaned_text.split())

# 创建一个DataFrame
df = pd.DataFrame(word_freq.most_common(100), columns=['Word', 'Frequency'])

# 定义Excel文件名
excel_file_name = 'all_files_word_frequency.xlsx'
save_path_excel = os.path.join(excel_folder_path, excel_file_name)

# 将DataFrame保存为Excel文件到指定路径
df.to_excel(save_path_excel, index=False)

# 显示词云
wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate_from_frequencies(word_freq)

plt.figure(figsize=(15, 7.5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 不显示坐标轴
plt.title('Word Cloud for All Files', fontsize=14)

# 定义词云图片文件名
wordcloud_file_name = 'all_files_wordcloud.png'
save_path_wordcloud = os.path.join(wordcloud_folder_path, wordcloud_file_name)

# 保存包含标题的词云图片到指定路径
plt.savefig(save_path_wordcloud, bbox_inches='tight', pad_inches=0.1)

# 显示词云
plt.show()

print(f'Saved {excel_file_name} to {excel_folder_path}')
print(f'Saved {wordcloud_file_name} to {wordcloud_folder_path}')