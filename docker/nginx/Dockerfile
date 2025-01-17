# 使用官方的nginx镜像作为基础镜像
FROM nginx:latest

# 安装Python3和pip
RUN apt-get update && \
    apt-get install -y curl git python3 python3-pip tcpdump iputils-ping 
RUN sudo apt install -y net-tools nmap avahi-daemon avahi-utils dnsutils dbus
RUN sudo ln -sf /usr/bin/python3 /usr/bin/python 
RUN sudo apt clean && rm -rf /var/lib/apt/lists/*

# 安装Python库
RUN pip install requests bottle paramiko --break-system-packages
RUN mkdir -p /home/gvsun
RUN mkdir -p /root/.config/code-server

COPY ./install.sh /root/.config/code-server/install.sh
COPY ./code-server/config.yaml /root/.config/code-server/config.yaml
RUN bash /root/.config/code-server/install.sh
RUN cd /home/gvsun && git clone https://github.com/nanhai-gvsun/webplatform.git
# 暴露80端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]