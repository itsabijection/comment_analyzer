#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 13:06:14 2018

@author: benjamin
"""
import gensim
from gensim.models import word2vec
import os
import re
import dill as pickle
import logging
from collections import defaultdict as dd
from word_count import find_month

months=["Jan", "Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def trim(word):
    return(re.sub(r'[^A-Za-z \']', '', word).lower())
config_file=os.getcwd()+"/../locations.conf"
f=open(config_file, "r")
a=f.read().split("\n")
direc_prefix=a[0]
site_list=["atlantic", "breitbart", "motherjones", "thehill"]
day_finder=re.compile(r".*_(\d{1,3})\.txt")
result_storage_direc=a[1]
class sentences(object):
    def __init__(self, file_list):
        self.file_list=file_list
    def __iter__(self):
        for file in file_list:
            try:
                comment_list=pickle.load(open(file, "rb"))
                for j in comment_list:
                        yield(trim(j["raw_message"]).split())
            except:
                continue
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
comment_pattern=re.compile("^comments_(1000_)?2016.*")
prev_file=None
for site in site_list:
    site_d=site+"/"
    files=dd(list)
    for i in os.listdir(direc_prefix+site_d):
        if comment_pattern.match(i):
            files[find_month(int(day_finder.search(i).group(1)))].append(direc_prefix+site_d+i)
    for month in months:
        file_list=files[month]
        s=sentences(file_list)
        if prev_file is None:
            model=word2vec.Word2Vec(s, iter=10)
        else:
            model=gensim.models.Word2Vec.load(prev_file)
            model.train(s, iter=10, size=300, workers=10)
            prev_file=result_storage_direc+"{}2016{}.w2v".format(site,month)
        model.save(result_storage_direc+"{}2016{}.w2v".format(site,month))
