#!/bin/bash

# 启动 dbus
sudo mkdir -p /run/dbus
sudo dbus-daemon --system

# 启动 avahi-daemon
sudo avahi-daemon --daemonize

# 启动 nginx
sudo service nginx start
sudo bash /usr/local/bin/init_git.sh
# 启动 python后台服务
python /home/gvsun/webplatform/app.py &
