# Whisper (本地) — 语音识别与语音合成指南

本目录提供两类本地化示例：语音转文字（STT）与文字转语音（TTS）。目标是能在离线或本地环境运行（使用本地模型或离线引擎）。

目录结构
- `stt_faster_whisper.py`：基于 `faster-whisper` 的本地语音转文字示例（Python）。
- `tts_pyttsx3.py`：基于 `pyttsx3` 的离线文字转语音示例（Python，跨平台）。

快速开始（macOS / Linux / Windows）

1) 建议创建虚拟环境并激活：

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
\.venv\Scripts\activate   # Windows (PowerShell)
```

2) 安装依赖（示例）

```bash
pip install --upgrade pip
pip install faster-whisper pyttsx3
```

说明与可替换方案
- 语音识别（STT）可选：
  - `faster-whisper`：Python 接口，支持 CPU/GPU，本地加载 Whisper 模型（推荐用于 Python 项目）。
  - `whisper.cpp`：C/C++ 实现，适合嵌入式或无 Python 环境的场景。

- 语音合成（TTS）可选：
  - `pyttsx3`：纯离线，易用，依赖平台的 TTS 引擎（macOS 使用 NSSpeechSynthesizer，Windows 使用 SAPI，Linux 常用 espeak）。
  - `Coqui TTS` 或 `Mozilla TTS`：质量更高，但体积和依赖较多，适合需要更自然语音的场景。

使用示例

- STT（将 `input_audio.wav` 转为 `output.txt`）：

```bash
python agents/whisper/stt_faster_whisper.py --model small --input input_audio.wav --output output.txt
```

- TTS（将文本保存为 `out.wav`）：

```bash
python agents/whisper/tts_pyttsx3.py --text "你好，世界" --output out.wav
```

注意事项
- 模型文件：`faster-whisper` 会在首次运行时自动下载模型到缓存目录，请确保存储空间充足。
- 在无 GPU 的情况下，选择小型或基础模型（如 `small`、`base`）以降低内存占用。
- 若需更高质量的 TTS，参考 Coqui TTS 官方文档并替换示例脚本。

更多帮助
如需我把 `whisper.cpp` 或 `Coqui TTS` 的完整本地部署示例也加入此目录，告诉我即可。 
 
---

## Coqui TTS (可选，本地高质量 TTS)

此处包含一个使用 Coqui TTS (`TTS` Python 包) 的简单示例。Coqui TTS 提供比 `pyttsx3` 更自然的语音，但依赖较多（例如 `torch`）并需要下载模型权重。

安装示例（建议在虚拟环境中）：

```bash
pip install TTS torch
```

使用示例：

```bash
python agents/whisper/coqui_tts_example.py --text "你好，Coqui TTS" --output coqui_out.wav
```

注意：Coqui TTS 在首次运行时会下载模型。若要指定模型，请使用 `--model` 参数（参考 Coqui TTS 模型名称）。
