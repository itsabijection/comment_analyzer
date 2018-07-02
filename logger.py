#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 09:50:11 2018

@author: benjamin
"""
from os import getcwd, getppid
from time import time
config_file=getcwd()+"/../locations.conf"
f=open(config_file, "r")
a=f.read().split("\n")
logfile=a[2]
def logger(q):
    f=open(logfile, "w")
    while True:
        if getppid==1:
            f.write("Parent process killed at {}".format(time()))
            break
        m=q.get()
        if m=="kill":
            break
        f.write(str(m) + "\n")
        f.flush()
    f.close()