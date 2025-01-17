#!/bin/bash

# 启动 dbus
sudo mkdir -p /run/dbus
sudo dbus-daemon --system

# 启动 avahi-daemon
sudo avahi-daemon --daemonize

# 启动 nginx
sudo service nginx start
sudo bash /usr/local/bin/init_git.sh
# 启动 code-server
code-server --bind-addr 0.0.0.0:8443 --auth none