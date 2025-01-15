#!/bin/bash

# 检查参数数量
if [ $# -ne 3 ]; then
    echo "用法: $0 <项目名> <分支> <版本>"
    echo "示例: $0 myproject master 1.0.0"
    exit 1
fi

# 获取参数
PROJECT=$1
BRANCH=$2
VERSION=$3

# 检查项目目录是否存在
if [ ! -d "$PROJECT" ]; then
    echo "错误: 项目目录 '$PROJECT' 不存在"
    exit 1
fi

# 检查项目目录下是否存在 publish.sh
if [ ! -f "$PROJECT/publish.sh" ]; then
    echo "错误: 在项目目录 '$PROJECT' 中未找到 publish.sh"
    exit 1
fi

# 确保 publish.sh 有执行权限
chmod +x "$PROJECT/publish.sh"

# 执行项目的 publish.sh
echo "正在执行 $PROJECT/publish.sh，分支=$BRANCH，版本=$VERSION"
cd "$PROJECT" && ./publish.sh -b "$BRANCH" -v"$VERSION"

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "项目 $PROJECT ($BRANCH) 版本 $VERSION 发布成功"
    exit 0
else
    echo "项目 $PROJECT 发布失败"
    exit 1
fi