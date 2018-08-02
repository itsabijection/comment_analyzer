#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 16:16:19 2018

@author: benjamin
"""
#%%
import dill as pickle
from collections import defaultdict as dd
from nltk.probability import FreqDist as fd
#%%
#site, year, month, word, POS
direc="/home/benjamin/sfi/project_stuff/data/clean/"
years=["2016"]#,"2017"]
months=["Jan", "Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
site_list=["atlantic","breitbart","thehill","motherjones"]
all_words=[]
for year in years:
    for month in months:
        p=pickle.load(open(direc+month+year+"stats.pkl", "rb"))
        for site in site_list:
            all_words.extend(p[0][site][year][month].keys())
print("1")
#%%
p=dd(lambda: dd(lambda: dd(fd)))
for site in site_list:
    for year in years:
        for month in months:
            a=pickle.load(open(direc+month+year+"stats.pkl", "rb"))
            p[site][year][month]=a[0][site][year][month]
print("1")
#%%      
with open(direc+"nfreqs.csv", "w") as f:
    for i,word in enumerate(all_words):
        st="{},".format(word)
        m=0
        for year in years:
            for month in months:
                for site in site_list:
                    if p[site][year][month][word] > 10:
                        st+="{},".format(p[site][year][month][word])
                        m=max(m,p[site][year][month][word])
                    else:
                        st+=","
            if m>10:
                st+="\n"
                f.write(st)