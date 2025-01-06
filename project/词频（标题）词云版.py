# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 21:31:15 2025

@author: Ting
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 21:31:15 2025

@author: Ting
"""

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

# 如果Excel文件夹不存在，则创建
if not os.path.exists(excel_folder_path):
    os.makedirs(excel_folder_path)

# 指定保存词云图片的文件夹路径
wordcloud_folder_path = 'D:/A NLP/storage/dh/Word Cloud'

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

# 定义 all_titles 文件路径
all_titles_path = os.path.join('D:/A NLP/storage/dh/all titles', 'all_titles_text.txt')

# 检查all_titles.txt文件是否存在，如果存在则删除并重新创建
if os.path.exists(all_titles_path):
    os.remove(all_titles_path)
with open(all_titles_path, 'w', encoding='utf-8') as f:
    print("Existing 'all_titles.txt' file deleted and recreated.")

# 提取所有标题并保存到一个新的txt文件中
all_titles = ""
for txt_file in txt_files:
    # 定义文件路径
    file_path = os.path.join(folder_path, txt_file)
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # 检查lines列表是否为空
        if lines:  # 如果不为空
            # 假设标题是第一行，去除两端空白并添加到all_titles中
            title = lines[0].strip()
            all_titles += title + " "

# 创建一个新的txt文件保存所有标题
with open(all_titles_path, 'w', encoding='utf-8') as f:
    f.write(all_titles)
    print("'all_titles.txt' file has been created with new content.")

# 对新的txt文档进行词频统计
if all_titles:  # 确保all_titles不为空
    cleaned_titles = text_clean(all_titles)
    word_freq = Counter(cleaned_titles.split())
    # 创建一个DataFrame
    df = pd.DataFrame(word_freq.most_common(100), columns=['Word', 'Frequency'])
    # 定义Excel文件名
    excel_file_name = "all_titles.xlsx"
    save_path_excel = os.path.join(excel_folder_path, excel_file_name)
    # 将DataFrame保存为Excel文件到指定路径
    df.to_excel(save_path_excel, index=False)

# 显示词云
wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate_from_frequencies(word_freq)

plt.figure(figsize=(15, 7.5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 不显示坐标轴
plt.title('Word Cloud for All Titles', fontsize=14)

# 定义词云图片文件名
wordcloud_file_name = 'all_titles_wordcloud.png'
save_path_wordcloud = os.path.join(wordcloud_folder_path, wordcloud_file_name)

# 保存包含标题的词云图片到指定路径
plt.savefig(save_path_wordcloud, bbox_inches='tight', pad_inches=0.1)

# 显示词云
plt.show()

print(f'Saved {excel_file_name} to {excel_folder_path}')
print(f'Saved {wordcloud_file_name} to {wordcloud_folder_path}')
