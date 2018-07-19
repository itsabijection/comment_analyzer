#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 09:50:11 2018

@author: benjamin
"""
from os import getcwd
config_file=getcwd()+"/../locations.conf"
f=open(config_file, "r")
a=f.read().split("\n")
logfile=a[2]
def logger(q):
    f=open(logfile, "w")
    while True:
        m=q.get()
        if m=="kill":
            break
        f.write(str(m) + "\n")
        f.flush()
    f.close()