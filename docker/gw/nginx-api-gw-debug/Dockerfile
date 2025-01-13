# 使用 code-server 官方镜像作为基础镜像
FROM codercom/code-server:latest
# 安装 nginx 和 python3
RUN sudo apt update
RUN sudo apt install -y curl tcpdump nginx python3 python3-pip
RUN sudo ln -sf /usr/bin/python3 /usr/bin/python
RUN pip install requests bottle paramiko --break-system-packages
RUN sudo apt clean
RUN sudo rm -rf /var/lib/apt/lists/*

# 复制初始化脚本到容器中
COPY init.sh /usr/local/bin/init.sh

# 暴露 code-server 和 nginx 的端口
EXPOSE 8443 80 443

# 添加挂载目录
VOLUME "/etc/localtime" "/etc/timezone" "/etc/nginx/nginx.conf" "/etc/nginx/conf.d" "/var/log/nginx" "/var/nginx/cache" "/home/gvsun/webplatform" "/home/coder/.config/code-server/config.yaml"

# 设置启动命令
CMD ["bash", "/usr/local/bin/init.sh"]
ENTRYPOINT ["bash", "/usr/local/bin/init.sh"]