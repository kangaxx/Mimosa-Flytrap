#!/bin/bash
# Homebrew 安装 Ollama 并配置 OpenAI 兼容层
set -e  # 出错时终止脚本

# 1. 更新 Homebrew（可选，确保最新）
echo "=== 1. 更新 Homebrew ==="
brew update

# 2. 安装 Ollama
echo -e "\n=== 2. 安装 Ollama ==="
brew install ollama

# 3. 停止现有 Ollama 服务（避免冲突）
echo -e "\n=== 3. 停止现有 Ollama 服务 ==="
brew services stop ollama || true

# 4. 修改 Ollama 的 brew 启动配置，添加 OpenAI 兼容层环境变量
echo -e "\n=== 4. 配置 OpenAI 兼容层 ==="
# 找到 Ollama 的 plist 配置文件路径
OLLAMA_PLIST=$(find /opt/homebrew/Cellar/ollama/ -name "homebrew.mxcl.ollama.plist" | head -1)
if [ -z "$OLLAMA_PLIST" ]; then
    echo "错误：未找到 Ollama 的 plist 配置文件"
    exit 1
fi

# 备份原配置文件
cp "$OLLAMA_PLIST" "$OLLAMA_PLIST.bak"

# 检查是否已添加 EnvironmentVariables 节点，避免重复添加
if ! grep -q "EnvironmentVariables" "$OLLAMA_PLIST"; then
    # 插入 EnvironmentVariables 节点（核心：开启 OLLAMA_HOST=0.0.0.0）
    sed -i '' '/<key>Label<\/key>/a\
  <key>EnvironmentVariables<\/key>\
  <dict>\
    <key>OLLAMA_HOST<\/key>\
    <string>0.0.0.0<\/string>\
  <\/dict>' "$OLLAMA_PLIST"
    echo "已为 Ollama 添加 OpenAI 兼容层配置"
else
    echo "Ollama 已配置 OpenAI 兼容层，无需重复修改"
fi

# 5. 启动 Ollama 服务（自动以兼容模式运行）
echo -e "\n=== 5. 启动 Ollama 服务 ==="
brew services start ollama

# 6. 验证安装和兼容层是否生效
echo -e "\n=== 6. 验证安装结果 ==="
# 检查 Ollama 版本
ollama --version && echo "✅ Ollama 安装成功"

# 检查服务状态
brew services list | grep ollama && echo "✅ Ollama 服务已启动"

# 验证 OpenAI 兼容层接口
if curl -s http://localhost:11434/v1/models > /dev/null; then
    echo "✅ OpenAI 兼容层配置生效"
else
    echo "⚠️ OpenAI 兼容层验证失败，请检查配置"
fi

echo -e "\n=== 安装完成 ==="
echo "使用说明："
echo "1. 启动/停止 Ollama：brew services start/stop ollama"
echo "2. 重启 Ollama：brew services restart ollama"
echo "3. 下载模型：ollama pull deepseek-r1"
echo "4. 测试兼容层：curl http://localhost:11434/v1/models"
