# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 14:30:23 2024

@author: Ting
"""

# 停用词的过滤

# 下载nltk停用词数据
# import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
# print(stopwords.readme().replace('\n',''))

# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.text import Text
# str1 = "Today's weather is good, very windy and sunny, we have no classes in the afternoon,We have to play basketball tomorrow"
# tokens = word_tokenize(str1)
# tokens = [word.lower() for word in tokens]
# t1 = Text(tokens)
# from nltk.corpus import stopwords
# test_words = [word.lower() for word in tokens] 
# test_words_set = set(test_words)
# # print(test_words_set.intersection(set(stopwords.words('english'))))

# # 过滤停用词
# filtered = [w for w in test_words_set if (w not in stopwords.words('english'))]
# print(filtered) # ['afternoon', 'tomorrow', 'basketball', 'sunny', 'classes', "'s", 'windy', ',', 'play', 'weather', 'today', 'good']

