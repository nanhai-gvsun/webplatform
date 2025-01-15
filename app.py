#！/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,time
from module.services import *

runtime=Edict(
    path=os.path.dirname(os.path.abspath(__file__))
)

# 配置文件是etc/conf/apps/webrelease.json
runtime.config.filepath="etc/conf/apps/webrelease.json"
runtime.config.default.filepath="etc/default/webrelease.json"
if not os.path.exists(os.path.join(runtime.path,runtime.config.filepath)):
    print("配置文件不存在")
    os.system(f"cp {runtime.path}/{runtime.config.default.filepath} {runtime.path}/{runtime.config.filepath}")    





