#coding=utf-8
import os
__author__ = "zhaichuang"

files = os.listdir("Client_shfiles")
for f in files:
    with open("Client_shfiles/%s"%f,"r") as f2:
            fcontent=f2.readlines()[1]
            if "--data" not in fcontent:
                pass
                #print(fcontent.split("-u")[1].split("?")[1].split("&")[:2])
            else:
                print(fcontent)
