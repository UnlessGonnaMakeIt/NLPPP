# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:47:57 2024

@author: Ting
"""

# 数据清洗实例
import re
from nltk.corpus import stopwords
from nltk import word_tokenize

# 输入数据
s = "    RT @Amila #Test\nTom\'s newly listed Co   &amp; Mary\'s unlisted    Group to supply tech for nlTK. \nh $AAPL https:// t.co/x34afsfQsh"

# 指定停用词
cache_english_stopwords = stopwords.words('english')

def text_clean(text):
    print('原始数据:',text,'\n')
    # 去掉HTML标签(e.g. &amp)
    text_no_special_entities = re.sub(r'\&\w*;|#\w*|@\w*','',text)
    print('去掉特殊标签后的：',text_no_special_entities,'\n')

    # 去掉一些价值符号
    text_no_tickers = re.sub(r'\$\w*','',text_no_special_entities)
    print('去掉价值符号后的：',text_no_tickers,'\n')
    
    # 去掉超链接
    text_no_hyperlinks = re.sub(r'https?:\/\/.*\/\w*','',text_no_tickers)
    print('去掉超链接后的',text_no_hyperlinks,'\n')
    
    # 去掉小词
    text_no_small_words = re.sub(r'\b\w{1,2}\b','',text_no_hyperlinks)
    print('去掉小词后的：',text_no_small_words,'\n')
    
    # 去掉多余的空格
    text_no_whitespace = re.sub(r'\s\s+',' ',text_no_small_words)
    text_no_whitespace = text_no_whitespace.lstrip('')
    print('去掉多余空格后的：',text_no_whitespace,'\n')
    
    # 分词
    tokens = word_tokenize(text_no_whitespace)
    print('分词结果：',tokens,'\n')
    
    # 去停用词
    list_no_stopwords = [i for i in tokens if i not in cache_english_stopwords]
    print('去停用词后的：',list_no_stopwords,'\n')
    
    # 过滤后结果
    text_filtered = ' '.join(list_no_stopwords)
    print('过滤后：',text_filtered)
text_clean(s)