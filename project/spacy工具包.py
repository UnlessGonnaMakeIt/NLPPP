# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:58:25 2025

@author: Ting
"""

# import spacy
# nlp = spacy.load("en_core_web_sm")
# doc = nlp('Weather is good,very windy and sunny. We have no class in the afternoon.')

# # 分词
# for token in doc:
#     print(token)
    
# # 分句
# for sent in doc.sents:
#     print(sent)

# 词性
# for token in doc:
#     print('{}:{}'.format(token, token.pos_))
    
# 命名体识别
# doc_2 = nlp('I went to Paris where I met my old friend Jack from England')
# for ent in doc_2.ents:
#     print('{}:{}'.format(ent, ent.label_))


# import spacy
# from spacy import displacy
# import matplotlib.pyplot as plt
# from io import StringIO
# import os

# nlp = spacy.load("en_core_web_sm")
# doc = nlp('I went to Paris where I met my old friend Jack from England')

# # 调整显示选项
# options = {
#     "distance": 150,  # 增大实体之间的间距
#     "compact": False   # 不使用紧凑模式
# }

# # 将结果保存为 HTML 字符串
# html = displacy.render(doc, style='ent', options=options)

# # 将 HTML 保存为临时文件
# temp_html = 'temp.html'
# with open(temp_html, 'w', encoding='utf-8') as f:
#     f.write(html)

# # 使用命令行工具将 HTML 转换为 PNG 图像，并指定图像尺寸和放大比例
# temp_png = 'temp.png'
# os.system(f'wkhtmltoimage --width 1600 --height 800 --zoom 2.5 {temp_html} {temp_png}')

# # 读取并显示图像
# img = plt.imread(temp_png)
# plt.figure(figsize=(10, 5))  # 调整 matplotlib 的显示尺寸
# plt.imshow(img)
# plt.axis('off')
# plt.show()

# # 删除临时文件
# os.remove(temp_html)
# os.remove(temp_png)

# 例子（找到书中所有人物的名字）
import spacy
import pdfplumber
from collections import Counter

# 加载 spaCy 模型
nlp = spacy.load("en_core_web_sm")

def read_pdf(file_name):
    """
    从 PDF 文件中提取文本内容.
    """
    text = ""
    with pdfplumber.open(file_name) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def process_text(text):
    """
    使用 spaCy 处理文本并提取句子.
    """
    processed_text = nlp(text)
    sentences = [s.text for s in processed_text.sents]
    return sentences

def find_names(sentences):
    """
    找到文本中出现频率最高的前10个人名.
    """
    c = Counter()
    for sentence in sentences:
        doc = nlp(sentence)  # 将句子转换为 spaCy 文档对象
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                c[ent.lemma_] += 1
    return c.most_common(10)

# 读取 PDF 文件
pdf_file_name = 'D:/e books/Pride and Prejudice (Jane Austen) (Z-Library).pdf'
text = read_pdf(pdf_file_name)

# 处理文本并提取句子
sentences = process_text(text)

# 打印句子数量
print(f"Number of sentences: {len(sentences)}")

# 打印前几个句子
for i, sentence in enumerate(sentences[:5]):
    print(f"Sentence {i+1}: {sentence}")

# 找到并打印出现频率最高的前10个人名
print(find_names(sentences))