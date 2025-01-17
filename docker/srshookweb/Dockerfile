FROM ossrs/srs:v6.0.155

# 设置环境变量避免交互式配置
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 安装Python3、pip和基本网络工具
RUN apt-get update && \
    apt-get install -y curl git python3 python3-pip net-tools iputils-ping 
RUN ln -sf /usr/bin/python3 /usr/bin/python 

# 安装网络调试工具
RUN apt install -y tcpdump nmap avahi-daemon avahi-utils dnsutils dbus
# 清理安装备份
RUN apt clean && rm -rf /var/lib/apt/lists/*

# 安装Python库
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# debug版安装code-server
RUN mkdir -p /root/.config/code-server
COPY ./install.sh /root/.config/code-server/install.sh
COPY ./code-server-config.yaml /root/.config/code-server/config.yaml
RUN bash /root/.config/code-server/install.sh

# 克隆webplatform
RUN mkdir -p /home/gvsun
RUN cd /home/gvsun && git clone https://github.com/nanhai-gvsun/webplatform.git
WORKDIR /home/gvsun/webplatform

# 继承基础镜像的配置
VOLUME /usr/local/srs/objs/nginx/html
VOLUME /usr/local/srs/conf

# 开放端口
EXPOSE 1935 1985 8080 9000 5060 8000/udp

# 设置工作目录
WORKDIR /usr/local/srs

# 修改启动命令为执行启动脚本
CMD ["bash", "/home/gvsun/webplatform/docker/srshookweb/init.sh"]
ENTRYPOINT ["bash", "/home/gvsun/webplatform/docker/srshookweb/init.sh"]