#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:14:36 2018

@author: benjamin
"""
import re
import os

config_file=os.getcwd()+"/../locations.conf"
f=open(config_file, "r")
a=f.read().split("\n")
direc_prefix=a[0]
site_list=["atlantic", "breitbart", "motherjones", "thehill"]
result_storage_direc=a[1]

pattern=re.compile("^comment.*")
files=[]
for d in site_list:
    for i in os.listdir(direc_prefix+d+"/"):
        if pattern.match(i):
            files.append(direc_prefix+d+"/"+i)