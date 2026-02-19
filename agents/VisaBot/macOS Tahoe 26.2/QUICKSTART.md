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

## 后续操作建议

- 修改 `.env` 中模型参数（如温度、模型名）以适配你的场景。
- 将常见问题沉淀到独立文档，方便复用 prompt。
- 若要接入前端/接口服务，可直接复用 `run_visabot.py` 里的 `ask_visabot()` 方法。
