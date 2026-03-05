#!/usr/bin/env bash
set -euo pipefail

echo "==> 开始安装 AgentS (通过 pip 安装)..."

echo "==> 检查 Python 3.11 是否已安装..."
if ! command -v python3.11 &> /dev/null; then
    echo "未找到 python3.11，请先安装 Python 3.11 (例如: brew install python@3.11)"
    exit 1
fi

echo "==> 准备安装目录: .venv"

echo "==> 使用 Python 3.11 创建并激活虚拟环境..."
python3.11 -m venv .venv
source .venv/bin/activate

echo "==> 升级 pip 并安装 AgentS..."
pip install --upgrade pip
pip install gui-agents

echo "==> AgentS 安装准备完成！"
echo "请运行 'source \".venv/bin/activate\"' 来激活虚拟环境。"
