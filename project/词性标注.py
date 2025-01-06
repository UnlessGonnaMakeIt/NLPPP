# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 15:14:25 2024

@author: Ting
"""

# 词性标注
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


# from nltk import pos_tag
# tags = pos_tag(tokens)
# print(tags)

# 分块
import nltk
from nltk.chunk import RegexpParser
sentence = [('the','DT'),('little','JJ'),('yellow','JJ'),('dog','NN'),('died','VBD')]
grammar = "MY_NP: {<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(grammar) # 生成规则
result = cp.parse(sentence) # 进行分块
print(result)
result.draw()

#命名实体识别

# import nltk
# from nltk import ne_chunk
# from nltk.tokenize import word_tokenize
# from nltk import pos_tag
# import matplotlib.pyplot as plt
# sentence = 'Edison went to Tsinghua University today.'
# result = ne_chunk(pos_tag(word_tokenize(sentence)))
# print(result)
# result.draw()
