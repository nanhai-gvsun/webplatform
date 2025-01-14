#！/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,time
from module.services import *

path=os.path.dirname(os.path.abspath(__file__))
runtime=Edict()
if not os.path.exists(os.path.join(path,"etc/conf/apps/webrelease.json")):
    print("配置文件不存在")
    os.system(f"cp {path}/etc/default/webrelease.json {path}/etc/conf/apps/webrelease.json")    

# runtime.conf=File(path=f"{path}/etc/conf/apps/webrelease.json",autoLoad=True)



