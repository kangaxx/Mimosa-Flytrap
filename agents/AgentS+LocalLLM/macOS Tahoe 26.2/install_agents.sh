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

echo "==> 升级 pip 并安装 AgentS 及其依赖..."
pip install --upgrade pip
pip install gui-agents

echo "==> 检查并安装系统依赖 (tesseract)..."
if command -v brew &> /dev/null; then
    if ! command -v tesseract &> /dev/null; then
        echo "正在使用 Homebrew 安装 tesseract..."
        brew install tesseract
    else
        echo "tesseract 已安装。"
    fi
else
    echo "未找到 Homebrew，请手动安装 tesseract: https://brew.sh/"
fi

echo "==> AgentS 安装准备完成！"
echo "请运行 'source \".venv/bin/activate\"' 来激活虚拟环境。"
echo ""
echo "==== 关于本地 LLM 与无 Key 运行的说明 ===="
echo "您可以通过指定本地接口来完全在本地运行 (无需 OpenAI Key)。"
echo "对于主模型，可以通过 Ollama 或 vLLM 提供服务；"
echo "对于 Grounding 模型 (如 UI-TARS)，可使用本地 http://localhost:8080 等服务。"
echo ""
echo "如果是结合 Perplexica (本地搜索引擎/数据库)，可在 docker 部署中配置 OLLAMA 地址为 http://host.docker.internal:11434。"
echo ""
echo "【本地模型运行 CLI 示例】"
echo "agent_s \\"
echo "    --provider ollama \\"
echo "    --model <你的本地模型名, 例如 llama3> \\"
echo "    --ground_provider huggingface \\"
echo "    --ground_url http://localhost:8080 \\"
echo "    --ground_model ui-tars-1.5-7b \\"
echo "    --grounding_width 1920 \\"
echo "    --grounding_height 1080"
