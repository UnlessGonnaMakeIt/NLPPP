# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 17:41:26 2025

@author: Ting
"""

import os
import re
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
import webbrowser  # 用于打开文件链接

# 定义文件夹路径
folder_path = 'D:/A NLP/storage/dh/2024-12'
# 获取文件夹内所有txt文件
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
# Excel文件路径
excel_folder_path = 'D:/A NLP/storage/dh/excel'
# 词云图片文件夹路径
wordcloud_folder_path = 'D:/A NLP/storage/dh/Word Cloud'
# 结果保存路径
result_folder_path = 'D:/A NLP/storage/dh/research results/text'

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

# 加载Excel文件中的高频词
def load_word_frequencies(excel_file):
    df = pd.read_excel(excel_file)
    return df

# 检索指定单词在正文中的所有位置
def find_word_occurrences(word, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # 读取文件的全部内容
    positions = [m.start() for m in re.finditer(r'\b' + re.escape(word.lower()) + r'\b', content.lower())]
    return positions

# 显示检索框并处理检索功能
def search_word():
    search_word = entry_word.get().strip()
    if not search_word:
        messagebox.showwarning("输入错误", "请输入一个词汇进行检索")
        return

    # 遍历Excel中的高频词，查看是否包含检索的词
    df = load_word_frequencies(excel_file_path)
    matching_rows = df[df['Word'].str.lower() == search_word.lower()]

    if matching_rows.empty:
        messagebox.showinfo("无结果", f"词汇 '{search_word}' 没有出现在任何高频词列表中。")
        return

    # 输出为 HTML 格式
    output_html_path = os.path.join(result_folder_path, f"{search_word}_search_results_text.html")
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(f"<html><head><title>检索结果 - {search_word}</title>")
        html_file.write("""
        <style>
            .highlight {
                background-color: yellow;
                font-weight: bold;
            }
            .file-content {
                white-space: pre-wrap;
                word-wrap: break-word;
                font-family: monospace;
                font-size: 14px;
                border: 1px solid #ccc;
                padding: 10px;
                margin-top: 20px;
            }
            a {
                text-decoration: none;
            }
        </style>
        </head><body>""")
        html_file.write(f"<h1>词汇 '{search_word}' 出现的文件及次数：</h1><ul>")

        total_occurrences = 0

        for _, row in matching_rows.iterrows():
            word = row['Word']
            # 查找每个文件中该词出现的位置
            file_occurrences = []
            for txt_file in txt_files:
                file_path = os.path.join(folder_path, txt_file)
                positions = find_word_occurrences(word, file_path)
                if positions:
                    file_occurrences.append((txt_file, len(positions)))

            # 如果该词在文件中出现了，展示该文件和链接
            if file_occurrences:
                for file, count in file_occurrences:
                    file_path = os.path.join(folder_path, file)
                    file_content = get_file_content_with_highlights(file_path, search_word)

                    # 写入文件内容和链接
                    html_file.write(f"<li>文件: {file}, 出现次数: {count} ")
                    html_file.write(f"<a href='#' onclick='showContent(\"{file}\")'>点击查看</a></li>")
                    html_file.write(f"<div id='{file}' class='file-content' style='display:none'>{file_content}</div>")
                    total_occurrences += count

        # 显示总出现次数
        html_file.write(f"</ul><p><b>词汇 '{search_word}' 出现在正文中的总次数: {total_occurrences}</b></p>")

        # JavaScript 代码，动态显示内容并高亮检索词
        html_file.write("""
        <script>
            function showContent(fileId) {
                var contentDiv = document.getElementById(fileId);
                contentDiv.style.display = contentDiv.style.display === 'none' ? 'block' : 'none';
            }

            function highlightText(word) {
                var regex = new RegExp('\\b' + word + '\\b', 'gi');
                document.body.innerHTML = document.body.innerHTML.replace(regex, function(match) {
                    return '<span class="highlight">' + match + '</span>';
                });
            }
            highlightText('""" + search_word + """');
        </script>
        </body></html>""")

    # 提示用户结果已保存为HTML文件
    messagebox.showinfo("检索完成", f"检索结果已保存为 HTML 文件: {output_html_path}")

def get_file_content_with_highlights(file_path, search_word):
    """
    获取文件内容并将检索词高亮显示
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 高亮显示检索词
        highlighted_content = content.replace(search_word, f"<span class='highlight'>{search_word}</span>")
    return highlighted_content

# 主界面
root = tk.Tk()
root.title("高频词检索 - 正文")

# 创建文本框和按钮
label = tk.Label(root, text="请输入要检索的高频词：")
label.pack(padx=10, pady=10)

entry_word = tk.Entry(root, width=50)
entry_word.pack(padx=10, pady=10)

search_button = tk.Button(root, text="开始检索", command=search_word)
search_button.pack(padx=10, pady=10)

# 设置Excel文件路径
excel_file_path = os.path.join(excel_folder_path, "all_titles.xlsx")

root.mainloop()
