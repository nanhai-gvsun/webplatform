# -*- coding: utf-8 -*-
import sys,os

pwd=os.path.dirname(os.path.abspath(__file__))
libpath=os.path.abspath(os.path.join(pwd,'../module'))
if libpath not in sys.path:sys.path.append(libpath)

from services import *

data=Edict()
data.a.b.c=1
print(data)

# 初始化系统对象
system = System()

# 使用网络对象
pid = system.Net.getPidfromPort(8080)
print(f"PID from port 8080: {pid}")

# 使用进程对象
processes = system.Process.list()
print(f"Process list: {processes}")

# 使用控制台对象
system.Console.log("This is a log message")
system.Console.info("This is an info message")

# 使用文件系统对象
files = system.FileSystem.list("/path/to/directory")
print(f"Files in directory: {files}")

file_obj = system.FileSystem.get("/path/to/file.txt")
print(f"File content: {file_obj}")