FROM ubuntu:24.04

# 更新包列表并安装所需软件
RUN apt-get update && \
    apt-get install -y nano curl git python3 python3-pip net-tools iputils-ping openssh-server nodejs npm
RUN ln -sf /usr/bin/python3 /usr/bin/python 

# 安装网络调试工具
RUN apt install -y tcpdump nmap avahi-daemon avahi-utils dnsutils dbus
# 清理安装备份
RUN apt clean && rm -rf /var/lib/apt/lists/*
COPY ./init.sh /usr/local/bin/init.sh
# debug版安装code-server
RUN mkdir -p /root/.config/code-server
COPY ./install.sh /root/.config/code-server/install.sh
COPY ./config.yaml /root/.config/code-server/config.yaml
RUN bash /root/.config/code-server/install.sh
# RUN pip install wssh --break-system-packages
RUN mkdir -p /home/gvsun && cd /home/gvsun && git clone https://github.com/jacobgroundwater/node-wssh.git
# 创建SSH所需的目录
RUN mkdir /var/run/sshd

# 设置root密码为root（在生产环境中应该使用更安全的方式）
RUN echo 'root:gengshang' | chpasswd

# 允许root用户SSH登录（注意：在生产环境中不推荐这样做）
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH服务需要的环境变量
# ENV NOTVISIBLE "in users profile"
# RUN echo "export VISIBLE=now" >> /etc/profile


# COPY ./wssh /usr/local/bin/wssh
# RUN chmod +x /usr/local/bin/wssh
# 暴露SSH端口
EXPOSE 22

CMD ["bash", "/usr/local/bin/init.sh"]