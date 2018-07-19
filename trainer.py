#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 13:06:14 2018

@author: benjamin
"""
from gensim.models import word2vec
import os
import re
import sys
import dill as pickle
import logging

config_file=os.getcwd()+"/../locations.conf"
f=open(config_file, "r")
a=f.read().split("\n")
direc_prefix=a[0]
site_list=["atlantic", "breitbart", "motherjones", "thehill"]
result_storage_direc=a[1]
a=None
class sentences(object):
    def __init__(self, site, pattern):
        [self.site, self.pattern]=[site, pattern]
    def __iter__(self):
        for i in os.listdir(direc_prefix+self.site+"/"):
            #that file is fucked
            if self.pattern.match(i) and i!="comments_2016_248.txt" and i!="comments_2015_30.txt":
                comment_list=pickle.load(open(direc_prefix+self.site+"/"+i, "rb"))
                for j in comment_list:
                    global a
                    a=i
                    yield(j["raw_message"].split())
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
s=sentences("motherjones", re.compile(r"comments.*?"))
try:
    model=word2vec.Word2Vec(s, iter=10, min_count=2, size=300)
except:
    print(a)
model.save(result_storage_direc+"J16M.w2v")
