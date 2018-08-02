#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 14:27:34 2018

@author: benjamin
"""
from collections import defaultdict as dd
config_file="../locations.conf"
f=open(config_file, "r")
a=f.read().split("\n")
f.close()
f=open(a[3], "r")
a=[3,6,9,12,15]
emo=["hap","ang", "sad","fer","dis"]
word_ratings=dd(dd)
cat_line=f.readline()
for line in f.readlines():
    try:
        cols=line.split(",")
        word=cols[0]
        for i,e in zip(a,emo):
            word_ratings[word][e]=float(cols[i])
    except:
        continue
f.close()
def rate(word,model):
    if word not in model.wv.vocab:
        return 0
    score=dd(float)
    divisor=dd(float)
    for weighted_word in word_ratings.keys():
        if weighted_word in model.wv.vocab:
            #for e in emo:
                #score[e]+=abs(model.wv.similarity(word, weighted_word))*(word_ratings[weighted_word][e])
                #divisor[e]+=1
            e=max(word_ratings[weighted_word], key=lambda x: word_ratings[weighted_word][x])
            score[e]+=abs(model.wv.similarity(word, weighted_word))*(word_ratings[weighted_word][e])
            divisor[e]+=1
    for i in score.keys():
        score[i]/=(divisor[i]/100)
    return score