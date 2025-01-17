#!/bin/bash

# 启动 dbus
mkdir -p /run/dbus
dbus-daemon --system

# 启动 avahi-daemon
avahi-daemon --daemonize
git config --global user.email "lipy.sh@outlook.com"
git config --global user.name "lipy"

code-server &
cd /usr/local/srs && ./objs/srs -c ./conf/srs.conf
