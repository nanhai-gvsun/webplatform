# 使用官方的nginx镜像作为基础镜像
FROM nginx:latest

# 安装Python3、pip和基本网络工具
RUN apt-get update && \
    apt-get install -y curl git python3 python3-pip net-tools iputils-ping 
RUN ln -sf /usr/bin/python3 /usr/bin/python 

# 安装网络调试工具
RUN apt install -y tcpdump nmap avahi-daemon avahi-utils dnsutils dbus
# 清理安装备份
RUN apt clean && rm -rf /var/lib/apt/lists/*

# 安装Python库
RUN pip install requests bottle paramiko --break-system-packages

# debug版安装code-server
RUN mkdir -p /root/.config/code-server
COPY ./install.sh /root/.config/code-server/install.sh
COPY ./config.yaml /root/.config/code-server/config.yaml
RUN bash /root/.config/code-server/install.sh

# 克隆webplatform
RUN mkdir -p /home/gvsun
RUN cd /home/gvsun && git clone https://github.com/nanhai-gvsun/webplatform.git
WORKDIR /home/gvsun/webplatform

# 暴露80端口
EXPOSE 80 443

CMD ["bash", "/home/gvsun/webplatform/docker/nginx-api-gw/init.sh"]
ENTRYPOINT ["bash", "/home/gvsun/webplatform/docker/nginx-api-gw/init.sh"]