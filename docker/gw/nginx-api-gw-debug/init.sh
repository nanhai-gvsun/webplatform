#!/bin/bash

# 启动 nginx
sudo service nginx start
sudo git config --global user.email "lipy.sh@outlook.com"
sudo git config --global user.name "lipy"
# 启动 code-server
code-server --bind-addr 0.0.0.0:8443 --auth none