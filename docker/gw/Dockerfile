# 使用 code-server 官方镜像作为基础镜像
# 运行docker build时需要到/webplatform目录下进行，对应命令如下：
# docker build -t nginx-api-gw-debug:v1.0 -f docker/gw/nginx-api-gw-debug/Dockerfile .
FROM codercom/code-server:latest

# 复制代码到容器中
# RUN sudo mkdir -p /home/gvsun/webplatform
# COPY ./ /home/gvsun/webplatform
# 设置工作目录
WORKDIR /home/gvsun/webplatform

# 将当前目录下的所有文件和目录复制到容器中的 /home/gvsun/webplatform 目录
COPY . .

# 安装必要的工具
RUN sudo apt update 
RUN sudo apt install -y curl
RUN sudo apt install -y tcpdump 
RUN sudo apt install -y nginx 
RUN sudo apt install -y python3 
RUN sudo apt install -y python3-pip 
RUN sudo apt install -y iputils-ping 
RUN sudo apt install -y net-tools 
RUN sudo apt install -y nmap 
RUN sudo apt install -y avahi-daemon 
RUN sudo apt install -y avahi-utils 
RUN sudo apt install -y dnsutils 
RUN sudo apt install -y dbus
RUN sudo ln -sf /usr/bin/python3 /usr/bin/python 
RUN sudo apt clean 
RUN sudo rm -rf /var/lib/apt/lists/*
RUN sudo rm -rf /etc/nginx/nginx.conf 
RUN sudo ln -sf /home/gvsun/webplatform/etc/conf/apps/nginx.conf /etc/nginx/nginx.conf
RUN sudo rm -rf /etc/nginx/conf.d 
RUN sudo ln -sf /home/gvsun/webplatform/etc/conf/conf.d /etc/nginx/conf.d 
RUN sudo ln -sf /home/gvsun/webplatform/etc/logs /var/log/nginx 
RUN sudo mkdir -p /var/nginx
RUN sudo ln -sf /home/gvsun/webplatform/etc/cache /var/nginx/cache 
RUN sudo ln -sf /home/gvsun/webplatform/docker/gw/nginx-api-gw-debug/init.sh /usr/local/bin/init.sh 
# RUN sudo ln -sf /home/gvsun/webplatform/docker/gw/nginx-api-gw-release/init.sh /usr/local/bin/init.sh 
RUN sudo ln -sf /home/gvsun/webplatform/docker/gw/init_git.sh /usr/local/bin/init_git.sh 


# 安装 Python 依赖
# RUN pip install -r/home/gvsun/webplatform/docker/gw/requirements.txt --break-system-packages

# 暴露 code-server 和 nginx 的端口
EXPOSE 8443 80 443

# 添加挂载目录
VOLUME "/etc/localtime" "/etc/timezone" "/home/gvsun/webplatform"
# 设置启动命令
CMD ["bash", "/usr/local/bin/init.sh"]
ENTRYPOINT ["bash", "/usr/local/bin/init.sh"]
# 启动nginx
# CMD ["nginx", "-g", "daemon off;"]
