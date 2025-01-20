FROM ubuntu:24.04

# 更新包列表并安装所需软件
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    net-tools \
    iputils-ping \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# 创建SSH所需的目录
RUN mkdir /var/run/sshd

# 设置root密码为root（在生产环境中应该使用更安全的方式）
RUN echo 'root:root' | chpasswd

# 允许root用户SSH登录（注意：在生产环境中不推荐这样做）
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH服务需要的环境变量
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# 暴露SSH端口
EXPOSE 22

# 启动SSH服务
CMD ["/usr/sbin/sshd", "-D"] 