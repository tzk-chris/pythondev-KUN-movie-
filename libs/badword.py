# -*- coding: utf-8 -*-
"""
@File  : badword.py
@Author: Ekko
@Date  : 2020/7/10 2020/07/10
"""

import jieba
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import data

# data.path.append(u"D:\web_proj\movie_web20200704\movie_web\nltk_data")



t = "生活就像巧克力，你永远不知道下一块是什么味道~你他妈是个傻逼吧" \
    "hahahaha"\
    "人生苦短，我用python"
print(sent_tokenize(t))

# ret = jieba.lcut(t)
# print(ret)