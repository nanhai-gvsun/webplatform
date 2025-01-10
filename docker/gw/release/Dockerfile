# 使用官方的nginx镜像作为基础镜像
FROM nginx:latest

# 安装Python3和pip
RUN apt-get update && \
    apt-get install -y curl python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 安装Python库
RUN pip install requests bottle paramiko --break-system-packages
RUN mkdir -p /home/gvsun/webplatform
RUN ln -sf /usr/bin/puython3 /usr/bin/python
# 暴露80端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]
# 启动code-server和nginx
# CMD ["code-server","--config","/etc/code-server/config.yaml", "& nginx", "-"g "daemon off;"]