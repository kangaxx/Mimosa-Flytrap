# Quickstart — VisaBot (macOS Tahoe 26.2)

## 1) 安装系统依赖

```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

## 2) 创建 Python 环境并安装依赖

```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

说明：该脚本会自动安装 AutoGen（pyautogen）与 Playwright，并默认下载 Playwright 的 Chromium 浏览器。

如需安装全部浏览器（Chromium/Firefox/WebKit）：

```bash
PLAYWRIGHT_BROWSERS=all ./setup_environment.sh
```

## 3) 配置环境变量

首次执行 `setup_environment.sh` 会自动生成 `.env`。

- 默认使用 `ollama`：
  - 确保本地 Ollama 服务可用（默认 `http://localhost:11434`）
  - 按需修改 `OLLAMA_MODEL`
- 如果使用 `openai`：
  - 将 `MODEL_TYPE` 改为 `openai`
  - 填写 `OPENAI_API_KEY`

## 4) 运行检查脚本

```bash
chmod +x test_setup.sh
./test_setup.sh
```

默认不强制请求 Ollama/OpenAI（避免因服务未启动导致失败）。如需做端到端模型连通性检查：

```bash
RUN_LLM_SMOKE_TEST=1 ./test_setup.sh
```

可选：你也可以用下面命令快速激活虚拟环境（注意必须用 source）：

```bash
source ./activate_venv.sh
```

## 5) 启动 VisaBot

交互模式：

```bash
chmod +x start_visabot.sh
./start_visabot.sh
```

单次提问模式：

```bash
./start_visabot.sh --question "我申请旅游签证通常要准备哪些材料？"
```

## 6) （可选）用 Playwright 打开 TLS 网页

打开浏览器窗口（推荐：需要手动通过机器人验证，然后脚本会尝试选择上海）：

```bash
source ./.venv/bin/activate
python open_tls_page.py --no-headless --city Shanghai
```

Headless 打开并截图（适合无验证码页面；如有验证码建议用上面命令）：

```bash
source ./.venv/bin/activate
python open_tls_page.py --wait-until commit --screenshot tls.png --screenshot-timeout-ms 10000
```

说明：脚本不会绕过 CAPTCHA/机器人验证；需要你在浏览器里手动完成验证后回到终端按回车继续。

## 后续操作建议

- 修改 `.env` 中模型参数（如温度、模型名）以适配你的场景。
- 将常见问题沉淀到独立文档，方便复用 prompt。
- 若要接入前端/接口服务，可直接复用 `run_visabot.py` 里的 `ask_visabot()` 方法。
