# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 10:43:26 2025

@author: Ting
"""

import os
import spacy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict

# 加载 spaCy 的英文模型
nlp = spacy.load("en_core_web_sm")

# 存储文件标题的列表
def read_all_txt_file_name(directory):
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_names.append(filename)
    return file_names

# 存储文件内容的列表
def read_all_txt_file_content(directory):
    file_contents = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            full_path = os.path.join(directory, filename)
            with open(full_path, 'r', encoding='utf-8') as file:
                file_contents.append(' '.join(file.readlines()))
    return file_contents

# 指定目录路径
directory_path = 'D:/A NLP/storage/dh/2024-12'

# 读取文件名和内容
articles_name = read_all_txt_file_name(directory_path)
articles_content = read_all_txt_file_content(directory_path)

# 使用 spaCy 处理文本内容
articles_content_nlp = [nlp(art) for art in articles_content]

# 储存机构和地点实体的字典
organization_entity_dict = defaultdict(Counter)
location_entity_dict = defaultdict(Counter)

# 提取实体并计数
for article in articles_content_nlp:
    article_org = [ent.lemma_ for ent in article.ents if ent.label_ == 'ORG']
    article_locations = [ent.lemma_ for ent in article.ents if ent.label_ == 'GPE']
    organization_entity_dict['ORG'] += Counter(article_org)
    location_entity_dict['GPE'] += Counter(article_locations)

# 存储最常见的前10个实体的字典
top_10_organization_entities = organization_entity_dict['ORG'].most_common(10)
top_10_location_entities = location_entity_dict['GPE'].most_common(10)

# 创建一个字典来存储组织和地点之间的关系
organization_location_dict = defaultdict(Counter)

# 统计每个组织和地点之间的关系
for article in articles_content_nlp:
    orgs = [ent.lemma_ for ent in article.ents if ent.label_ == 'ORG']
    locations = [ent.lemma_ for ent in article.ents if ent.label_ == 'GPE']
    for org in orgs:
        for location in locations:
            if org in [entity for entity, _ in top_10_organization_entities] and location in [entity for entity, _ in top_10_location_entities]:
                organization_location_dict[org][location] += 1

# 将字典转换为 DataFrame
location_entity_df = pd.DataFrame.from_dict(dict(organization_location_dict), orient='index').fillna(0)

# 设置显示的最大列数
pd.set_option('display.max_columns', None)  # 显示所有列

# 创建热力图
plt.figure(figsize=(16, 9))
sns.heatmap(location_entity_df, annot=True, fmt=".0f", cmap='YlGnBu')
plt.title('Organization-Location Relationship Heatmap')

# 设置x轴标签的旋转角度和字体大小
plt.xticks(rotation=30, ha='center')  # 调整x轴标签的字体大小

# 自动调整子图参数，以确保布局合理
plt.tight_layout()

# 指定保存图像的路径和文件名
save_path = 'D:\\A NLP\\storage\\dh\\heatmap\\heatmap.png'

# 保存图像
plt.savefig(save_path, dpi=300, bbox_inches='tight')

plt.show()