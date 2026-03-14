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

## 部署方案一：使用 llama.cpp 部署 GGUF (强烈推荐给 Mac 用户)

对于 macOS (尤其是 M 系列 Apple Silicon 用户)，直接运行原生的 `vLLM` 或 `TGI` 常常会遇到算子缺失、显存支持不足或 SSL 证书问题。**使用基于 C++ 和 Metal 加速原生编译的 `llama.cpp` 是运行视觉大模型 (VLM) 效率最高、最稳妥的方法。**

### 1. 安装 llama.cpp

如果你的 Mac 装有 Homebrew，可以直接一键安装并启用 Metal (Apple GPU) 加速的 `llama.cpp` 环境：
```bash
brew install llama.cpp
# 这会自动安装 `llama-server` 命令行工具
```

### 2. 下载 UI-TARS 模型的 GGUF 格式

原生 HuggingFace 模型权重极大，在 Mac 上建议使用别人已经转好的 `*.gguf` 格式文件。
你可以打开浏览器前往 HuggingFace 搜索 `UI-TARS-1.5-7B GGUF`，例如：
* [lmstudio-community/UI-TARS-1.5-7B-GGUF](https://huggingface.co/lmstudio-community/UI-TARS-1.5-7B-GGUF) (如果社区有制作)
实际我找到了 https://huggingface.co/Mungert/UI-TARS-1.5-7B-GGUF
* 或者直接使用 `huggingface-cli` 下载对应尺寸的单文件（推荐 Q4_K_M 或 Q8_0 量化格式以兼顾速度与准度）

将文件下载并保存在你的电脑中，如 `~/models/ui-tars-v1.5-7b-q4_k_m.gguf`。

### 3. 启动 llama-server 提供 OpenAI APl 服务

打开终端，使用刚刚装好的 `llama-server` 暴露一个兼容 OpenAI API 的推理端口 (我们定为 `8080` 以适配 AgentS 默认逻辑)：

```bash
llama-server \
    -m ~/models/UI-TARS-1.5-7B-q4_k_m.gguf \
    --port 8080 \
    --host 0.0.0.0 \
    --ctx-size 8192 \
    -n -1 \
    -ngl 99 
```
* `-ngl 99`: 指令代表把所有的网络层都交由 Mac 的 GPU (Metal) 处理，这将极大提升推理速度。

### 4. 设置 llama-server 开机自启动 (可选)

如果在 Mac 上希望每次开机都能自动在后台启动这个 Grounding 服务，可以使用 macOS 自带的 `launchd` 机制：

1. **创建配置文件：**
   在终端中运行以下命令创建并极简打开配置文件：
   ```bash
   mkdir -p ~/Library/LaunchAgents
   touch ~/Library/LaunchAgents/com.mimosa.llama-server.plist
   open -e ~/Library/LaunchAgents/com.mimosa.llama-server.plist
   ```

2. **填入配置内容：**
   将以下 XML 内容粘贴到文本编辑器中。
   > **⚠️ 注意：你必须根据你本机的环境修改 `<array>` 内的文件路径！**
   > * `llama-server` 需要填绝对路径（可以用 `which llama-server` 查看，通常是 `/opt/homebrew/bin/llama-server`）。
   > * 模型也需要填绝对路径，不能用 `~`，例如要把 `YOUR_USERNAME` 换成你的用户名。

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.mimosa.llama-server</string>
       <key>ProgramArguments</key>
       <array>
           <!-- 替换为 llama-server 的绝对路径 -->
           <string>/opt/homebrew/bin/llama-server</string>
           <string>-m</string>
           <!-- 替换为模型的实际绝对路径 -->
           <string>/Users/YOUR_USERNAME/models/UI-TARS-1.5-7B-q4_k_m.gguf</string>
           <string>--port</string>
           <string>8080</string>
           <string>--host</string>
           <string>0.0.0.0</string>
           <string>--ctx-size</string>
           <string>8192</string>
           <string>-n</string>
           <string>-1</string>
           <string>-ngl</string>
           <string>99</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
       <key>StandardOutPath</key>
       <string>/tmp/llama-server.log</string>
       <key>StandardErrorPath</key>
       <string>/tmp/llama-server.err</string>
   </dict>
   </plist>
   ```

3. **加载并使其生效：**
   保存文件后，在终端执行以下命令加载自启项：
   ```bash
   launchctl load ~/Library/LaunchAgents/com.mimosa.llama-server.plist
   ```
   
> **提示：**
> 由于该服务在系统后台静默运行，如果你想实时查看其运行状况或测试日志，只需运行：
> `tail -f /tmp/llama-server.log` 或者查看报错日志 `tail -f /tmp/llama-server.err`。  
> 若要停止或清理：可以运行 `launchctl unload ~/Library/LaunchAgents/com.mimosa.llama-server.plist`。

---

## 部署方案二：使用 vLLM 或 llama.cpp 的 Python 替代方案

### 重要提示：macOS/MPS 对 Vision-Language (多模态) 模型支持说明
目前，vLLM 的 macOS (MPS) 后端对文本模型（如 Llama 3）支持良好，**但尚未完全实现对大多视觉多模态架构 (如基于 Qwen2-VL 架构的 UI-TARS) 的 MPS 全面支持。**如果在执行 vllm 命令时遇到了直接崩溃退出，通常是因为底层缺少针对 Mac 优化的多模态 CUDA 加速算子支持。

此时你有两种解决方向：
1. **使用纯 CPU (慢)：** 为 vllm 添加参数 ` --enforce-eager`。
2. **转移到 llama.cpp (强推给 Mac 用户):** 安装编译版 llama.cpp 来使用 GGUF 格式的 UI-TARS，速度和兼容性最佳。

### 【可选】vLLM 的强制启动方式

使用以下命令将 `UI-TARS-1.5-7B` 部署为 API 服务。如果在 macOS 上请务必添加 `--enforce-eager` 以关闭仅限英伟达的 CUDA Graphs 优化。（也可能还需要根据报错添加 `--device cpu`）。

```bash
# 如果遇到 SSL 证书验证报错 (certificate verify failed: unable to get local issuer certificate)
# Linux / macOS 下可临时关闭 SSL 验证：
export CURL_CA_BUNDLE=""
export REQUESTS_CA_BUNDLE=""

python3.11 -m vllm.entrypoints.openai.api_server \
    --model ByteDance-Seed/UI-TARS-1.5-7B \
    --port 8080 \
    --dtype float16 \
    --max-model-len 4096 \
    --trust-remote-code \
    --enforce-eager \
    --device cpu
```
> **注意 (macOS)**: 首次运行会自动从 HuggingFace 自动下载模型（约 14GB+），请保证网络畅通。如果在 Mac 运行，可能会使用系统内存替代显存，请至少准备 16GB 以上的可用内存。

---

## 部署方案三：使用 Hugging Face TGI (通过 Docker)

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

### 先决条件：检查模型服务是否就绪

在将接管权交给 `agent_s` 之前，必须确保本地的 Grounding 服务（如 `llama-server` 或 `vLLM`）已经成功启动并在监听对应端口。你可以通过以下两种方式进行验证，确认其具备接管条件：

1. **检查进程状态：**
   在终端运行 `ps aux | grep llama-server`，如果有相关的进程输出，说明服务已在后台或某个终端中存活运行。
2. **API 接口测试（最准确）：**
   打开一个新终端窗口，运行以下命令模拟调用接口：
   ```bash
   curl http://localhost:8080/v1/models
   ```
   如果终端能顺利返回一段包含模型名称的 JSON 数据（例如 `{"object":"list","data":[{"id":"...UI-TARS..."}]}` 或类似结构），这代表本地视觉大脑已经处于随时待命的接客状态，**完全具备了转交电脑接管权的先决条件**！

> **ℹ️ 关于 API Key 的设置说明：**
> 既然我们全程使用的是完全本地部署的 Ollama 和 llama-server 方案，**实际上并不需要真实的外部服务 API Key**。
> 但由于 `agent_s` 库内仍可能存在基础的格式非空校验，因此在执行下面启动命令前，如果你遇到提示未设置 Key 的错误，你可以随便赋值一个假的：
> ```bash
> export OPENAI_API_KEY="sk-local-dummy-key"
> ```

确认就绪后，您可以运行如下命令，正式将接管权交给本地模型（由于当前 `agent_s` 原生库不直接认 `ollama` 作为推理大模型 provider 的名称，你需要把它作为类似 `openai` 的 api 对接形式处理）：

```bash
agent_s \
    --provider openai \
    --model_url http://localhost:11434/v1 \
    --model deepseek-r1:8b \
    --ground_provider openai \
    --ground_url http://localhost:8080/v1 \
    --ground_model ByteDance-Seed/UI-TARS-1.5-7B \
    --grounding_width 1920 \
    --grounding_height 1080
```

### 核心参数解析
- `--provider openai` & `--model_url http://localhost:11434/v1`: 虽然大语言大脑我们使用的是本地的 Ollama，但在 `gui-agents` 库中并未原设对 `ollama` 这个 provider 名称的直接判断（会报不支持异常），因此我们使用它自带被支持的兼容 OpenAI 接口模式接入，通过 `--model_url` 指定到 Ollama 原生的 openai-compatible `/v1` 监听路径即可。
- `--model deepseek-r1:8b`：这个是你运行在 Ollama 里作思考决策用的大语言模型。
- `--ground_provider openai`：因为 `llama-server` 提供了兼容 OpenAI 的接口规范。如果是用 HuggingFace TGI 启动，则填 `huggingface` 和 `http://localhost:8080`。
- `--ground_url http://localhost:8080/v1`：此为您刚刚部署的本地推理进程的服务地址。
- `--ground_model`：需和你在本地 vLLM/TGI 启动时填写的 `--model` 名称保持一致。
- `--grounding_width` & `--grounding_height`：这应该填入你当前主屏幕的**实际分辨率**。UI-TARS 将会根据此分辨率返回它推断的鼠标点击坐标，如果分辨率填错，鼠标将点不到正确的位置！

## 性能与硬件需求说明
- **Mac (Apple Silicon)**: 16GB 统存可以勉强跑 7B 模型（如 M1/M2/M3 Pro），强烈建议使用 32GB 统存的 Mac 以确保 Grounding 模型推断加上录屏截取不会耗尽内存。
- **PC/Linux**: 推荐拥有 8GB 以上显存的独立显卡 (如 RTX 3060 12GB、RTX 4070、RTX 3090、macOS 相当于等效内存)。
