FROM ossrs/srs:v6.0.155

# 设置环境变量避免交互式配置
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 更新包列表并安装必要的软件包
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    nginx \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 验证安装
RUN python3 --version && \
    git --version && \
    nginx -v

# 创建app目录并复制启动脚本
COPY app /usr/local/srs/app
RUN chmod +x /usr/local/srs/app/start.sh

# 继承基础镜像的配置
VOLUME /usr/local/srs/objs/nginx/html
VOLUME /usr/local/srs/conf

# 开放端口
EXPOSE 1935 1985 8080 9000 5060 8000/udp

# 设置工作目录
WORKDIR /usr/local/srs

# 修改启动命令为执行启动脚本
CMD ["./app/start.sh"]