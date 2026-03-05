#!/bin/bash

# =================================================================
# Ubuntu 部署环境一键安装脚本
# 用于初始化 Mimosa Flytrap Spring Boot 服务端环境
# 适用系统: Ubuntu 20.04 LTS / 22.04 LTS 及以上
# =================================================================

set -e

echo "开始配置 Ubuntu 服务器环境..."

echo "1. 更新系统软件包列表..."
sudo apt-get update -y

echo "2. 安装 OpenJDK 17 (Spring Boot 3 推荐)..."
sudo apt-get install -y openjdk-17-jdk openjdk-17-jre

echo "3. 验证 Java 安装版本..."
java -version

echo "4. 为 Gradle Wrapper 赋予执行权限..."
if [ -f "gradlew" ]; then
    chmod +x gradlew
    echo "Gradle Wrapper 权限已配置。"
else
    echo "未找到 gradlew 文件，请确保在 server 根目录下执行该脚本。"
fi

echo "================================================================="
echo "环境配置完成！"
echo "您现在可以使用以下命令编译项目："
echo "./gradlew clean build -x test"
echo "================================================================="
