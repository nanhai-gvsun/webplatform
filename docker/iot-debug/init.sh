#!/bin/bash

# 启动 dbus
mkdir -p /run/dbus
dbus-daemon --system

# 启动 avahi-daemon
avahi-daemon --daemonize
git config --global user.email "lipy.sh@outlook.com"
git config --global user.name "lipy"

# wssh --address=0.0.0.0 --port=8888 & 
 cd /home/gvsun/node-wssh && npm start
# 启动SSH服务
/usr/sbin/sshd -D
