# 本地 Grounding (坐标定位) 服务配置指南

在 Agent-S 的运行过程中，**Grounding 模型** (例如 `UI-TARS-1.5-7B`) 负责视觉定位，即“把大语言模型 (LLM) 决定的动作，转化为屏幕上的真实像素坐标 (X, Y)”。

为了完全在本地、无须依赖云端 API 运行 Agent-S，你需要在本地启动一个暴露 HTTP 接口的模型推理服务。该服务需要支持 Vision-Language Model (多模态视觉模型)，并兼容 HuggingFace API / OpenAI API 格式。

本指南将介绍如何在本地（包括 macOS Apple Silicon 架构或 Linux/Windows 显卡环境）部署该服务。

---

## 推荐模型

官方推荐的 Grounding 模型是 **UI-TARS**，主要有两个参数版本：
- `ByteDance-Seed/UI-TARS-1.5-7B` (推荐绝大多数用户，普通显卡及 Mac M系列即可运行)
- `ByteDance-Seed/UI-TARS-7B` / `UI-TARS-72B` (需要极高显存的服务器)

---

## 部署方案一：使用 vLLM (推荐)

`vLLM` 是目前最流行的高性能大模型推理引擎之一，且支持 Vision-Language 模型，并原生支持 Apple Silicon (MPS 框架) 和 Nvidia CUDA。

### 1. 安装 vLLM

如果你使用 macOS (Apple Silicon)，建议在独立的虚拟环境中安装：
```bash
# 激活你的 Agent 虚拟环境或创建一个新的
source .venv/bin/activate

# 安装针对 macOS/MPS 优化的 vLLM 或者是通用版本
pip install vllm
```

### 2. 启动服务

使用以下命令将 `UI-TARS-1.5-7B` 部署为 OpenAI 兼容的 API 服务，默认端口为 `8000`（也可以指定 `8080`）：

```bash
python -m vllm.entrypoints.openai.api_server \
    --model ByteDance-Seed/UI-TARS-1.5-7B \
    --port 8080 \
    --dtype auto \
    --max-model-len 4096 \
    --trust-remote-code
```
> **注意 (macOS)**: 首次运行会自动从 HuggingFace 自动下载模型（约 14GB+），请保证网络畅通。如果在 Mac 运行，可能会使用系统内存替代显存，请至少准备 16GB 以上的可用内存。

---

## 部署方案二：使用 Hugging Face TGI (通过 Docker)

对于 Linux 服务器或可以运行 Docker 的环境（如通过 Docker Desktop），HuggingFace 官方的 Text Generation Inference (TGI) 非常稳定。

```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
    -v $PWD/data:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id ByteDance-Seed/UI-TARS-1.5-7B \
    --max-input-tokens 4096 \
    --max-total-tokens 8192
```
> **注意**: `--gpus all` 是 Linux/CUDA 下的参数。在 macOS Docker 环境中不支持直通 Apple GPU，会导致只能用 CPU 推理，速度极慢。因此 **macOS 本地用户推荐方案一 (vLLM) 或 使用 llama.cpp**。

---

## 在 Agent-S 中接入本地 Grounding 服务

当在终端看到本地服务端打出类似 `Uvicorn running on http://0.0.0.0:8080` 的日志后，即代表本地视觉定位大脑已启动。

随后，您可以打开另一个终端，使用如下启动参数将接管权交给本地模型：

```bash
agent_s \
    --provider ollama \
    --model llama3 \
    --ground_provider openai \
    --ground_url http://localhost:8080/v1 \
    --ground_model ByteDance-Seed/UI-TARS-1.5-7B \
    --grounding_width 1920 \
    --grounding_height 1080
```

### 核心参数解析
- `--ground_provider openai`：因为 `vLLM` 提供了兼容 OpenAI 的接口规范。如果是用 HuggingFace TGI 启动，则填 `huggingface` 和 `http://localhost:8080`。
- `--ground_url http://localhost:8080/v1`：此为您刚刚部署的本地推理进程的服务地址。
- `--ground_model`：需和你在本地 vLLM/TGI 启动时填写的 `--model` 名称保持一致。
- `--grounding_width` & `--grounding_height`：这应该填入你当前主屏幕的**实际分辨率**。UI-TARS 将会根据此分辨率返回它推断的鼠标点击坐标，如果分辨率填错，鼠标将点不到正确的位置！

## 性能与硬件需求说明
- **Mac (Apple Silicon)**: 16GB 统存可以勉强跑 7B 模型（如 M1/M2/M3 Pro），强烈建议使用 32GB 统存的 Mac 以确保 Grounding 模型推断加上录屏截取不会耗尽内存。
- **PC/Linux**: 推荐拥有 8GB 以上显存的独立显卡 (如 RTX 3060 12GB、RTX 4070、RTX 3090、macOS 相当于等效内存)。
