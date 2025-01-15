#!/bin/bash

# 读取当前目录
CURRENT_DIR=$(pwd)

#进入脚本所在目录
cd $(dirname $0)


# 默认值设置
DEFAULT_VERSION="1.0.0"
DEFAULT_BRANCH="release"

# 显示使用方法
show_usage() {
    echo "使用方法: $0 [-v version] [-b branch]"
    echo "选项:"
    echo "  -v: 版本号 (默认: $DEFAULT_VERSION)"
    echo "  -b: 分支类型 (debug/release, 默认: $DEFAULT_BRANCH)"
    echo "示例:"
    echo "  $0 -v 1.0.1 -b debug"
    echo "  $0 -v 2.0.0 -b release"
}

# 设置默认值
VERSION=$DEFAULT_VERSION
BRANCH=$DEFAULT_BRANCH
PROJECT="webplatform-gw"

# 解析命令行参数
while getopts "v:b:h" opt; do
    case $opt in
        v)
            VERSION=$OPTARG
            ;;
        b)
            BRANCH=$OPTARG
            if [[ "$BRANCH" != "debug" && "$BRANCH" != "release" ]]; then
                echo "错误: 分支类型必须是 debug 或 release"
                exit 1
            fi
            ;;
        h)
            show_usage
            exit 0
            ;;
        ?)
            show_usage
            exit 1
            ;;
    esac
done

# 确认信息
echo "准备发布以下配置："
echo "版本号: $VERSION"
echo "分支类型: $BRANCH"
echo ""
read -p "是否继续? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "操作已取消"
    exit 1
fi
# 生成dockerfile
if [[ "$BRANCH" == "debug" ]]; then
cat <<EOF > Dockerfile
FROM codercom/code-server:latest
WORKDIR /home/gvsun/webplatform
COPY . .
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
RUN sudo ln -sf /home/gvsun/webplatform/docker/gw/init.sh /usr/local/bin/init.sh 
RUN sudo ln -sf /home/gvsun/webplatform/docker/gw/init_git.sh /usr/local/bin/init_git.sh 


# 安装 Python 依赖
RUN pip install -r/home/gvsun/webplatform/docker/gw/requirements.txt --break-system-packages

# 暴露 code-server 和 nginx 的端口
EXPOSE 8443 80 443

# 添加挂载目录
VOLUME "/etc/localtime" "/etc/timezone" "/home/gvsun/webplatform"
# 设置启动命令
CMD ["bash", "/usr/local/bin/init.sh"]
ENTRYPOINT ["bash", "/usr/local/bin/init.sh"]
EOF
fi
if [[ "$BRANCH" == "release" ]]; then
cat <<EOF > Dockerfile
FROM nginx:latest
WORKDIR /home/gvsun/webplatform
COPY . .


# 安装Python3和pip
RUN apt-get update && \
    apt-get install -y curl python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 安装Python库
RUN pip install requests bottle paramiko --break-system-packages
RUN mkdir -p /home/gvsun/webplatform
RUN ln -sf /usr/bin/puython3 /usr/bin/python
# 暴露80端口
EXPOSE 80 443

# 添加挂载目录
VOLUME "/etc/localtime" "/etc/timezone" "/home/gvsun/webplatform"
# 设置启动命令
CMD ["bash", "/usr/local/bin/init.sh"]
ENTRYPOINT ["bash", "/usr/local/bin/init.sh"]
EOF
fi
# 生成docker-compose
echo "生成 docker-compose.yml..."
cat <<EOF > docker-compose.yml
version: '3.8'

services:
  web:
    image: $PROJECT-$BRANCH:$VERSION
    container_name: nginx-api-gw
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ../nginx/conf.d:/etc/nginx/conf.d
      - ../nginx/webplatform:/home/gvsun/webplatform
    networks:
      - my-bridge-network
    restart: unless-stopped

networks:
  my-bridge-network:
    driver: bridge
EOF
# 生成init.sh
echo "生成 init.sh..."
cat <<EOF > init.sh
#!/bin/bash

# 启动 dbus
sudo mkdir -p /run/dbus
sudo dbus-daemon --system

# 启动 avahi-daemon
sudo avahi-daemon --daemonize

# 启动 nginx
sudo service nginx start
sudo bash /usr/local/bin/init_git.sh

EOF
if [[ "$BRANCH" == "debug" ]]; then
    echo "code-server --bind-addr 0.0.0.0:8443 --auth none" >> init.sh
fi
if [[ "$BRANCH" == "release" ]]; then
    echo "python /home/gvsun/webplatform/app.py &" >> init.sh
fi



# 构建Docker镜像
echo "开始构建Docker镜像..."
# docker build \
#     --build-arg VERSION=$VERSION \
#     --build-arg BRANCH=$BRANCH \
#     -t gw:$VERSION-$BRANCH \
#     .

# # 检查构建结果
# if [ $? -eq 0 ]; then
#     echo "构建成功！"
#     echo "镜像标签: gw:$VERSION-$BRANCH"
# else
#     echo "构建失败！"
#     exit 1
# fi 

# 返回当前目录
cd $CURRENT_DIR
