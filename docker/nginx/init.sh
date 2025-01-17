#!/bin/bash

# 启动 dbus
sudo mkdir -p /run/dbus
sudo dbus-daemon --system

# 启动 avahi-daemon
sudo avahi-daemon --daemonize
sudo git config --global user.email "lipy.sh@outlook.com"
sudo git config --global user.name "lipy"

sudo code-server &
nginx -g "daemon off;"
