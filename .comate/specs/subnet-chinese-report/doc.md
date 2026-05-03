# Bittensor Subnet 中文综合报告生成器

## Requirement

开发一个 Python 脚本 `generate_subnet_report.py`，分析 `briefings/` 目录下所有 MD 简报文件，生成一份中文综合报告 MD 文件。

## Input

- `briefings/` 目录下约 104 个 `SN{id}_{name}.md` 文件
- 每个 MD 格式固定：
  - 一级标题：`# {子网名称}`
  - 元数据行：`- **子网名称**: ...` 和 `- **Git 项目**: [owner/repo](url)`
  - 二级标题：`## 硬件要求`，下接内容或 `无要求`

## Output

- 一个综合报告 MD 文件：`agents/bittensor/subnet_report.md`
- 报告内容（全中文）：
  1. **概览** — 总子网数、有 GitHub 项目数、有硬件要求数、无硬件要求数
  2. **子网总览表** — 按子网 ID 排序的表格，列：子网ID、子网名称、Git项目、硬件要求（有/无）
  3. **有硬件要求的子网详表** — 仅列出有硬件要求的子网，附加硬件要求摘要（取前 100 字）
  4. **分类统计** — 按硬件需求类型分类（GPU必需 / CPU为主 / 仅内存存储 / 无要求）

## Architecture

1. **解析 MD 文件** — 用正则提取子网名称、Git 项目、硬件要求段落
2. **分类** — 根据硬件要求内容中的关键词分类
3. **汇总** — 统计数量、生成表格
4. **渲染** — 用模板生成中文报告 MD

## Affected Files

| 文件 | 操作 |
|---|---|
| `agents/bittensor/generate_subnet_report.py` | 新建 |
| `agents/bittensor/subnet_report.md` | 输出 |

## Implementation Details

### MD 解析

```python
def parse_briefing(filepath: Path) -> dict:
    text = filepath.read_text(encoding="utf-8")
    # 子网名称：从一级标题提取
    name_match = re.search(r"^# (.+)$", text, re.MULTILINE)
    subnet_name = name_match.group(1) if name_match else ""
    # Git 项目：从 **Git 项目** 行提取
    git_match = re.search(r"\*\*Git 项目\*\*:\s*\[([^\]]+)\]\(([^)]+)\)", text)
    git_name = git_match.group(1) if git_match else ""
    git_url = git_match.group(2) if git_match else ""
    # 子网 ID：从文件名提取
    id_match = re.match(r"SN(\d+)", filepath.stem)
    subnet_id = int(id_match.group(1)) if id_match else 0
    # 硬件要求：取 ## 硬件要求 之后的内容
    hw_match = re.search(r"## 硬件要求\s*\n(.*)", text, re.DOTALL)
    hw_text = hw_match.group(1).strip() if hw_match else "无要求"
    has_hw = hw_text != "无要求"
    return {
        "subnet_id": subnet_id,
        "subnet_name": subnet_name,
        "git_name": git_name,
        "git_url": git_url,
        "has_hw": has_hw,
        "hw_text": hw_text,
    }
```

### 分类逻辑

```python
def classify_hw(hw_text: str) -> str:
    if hw_text == "无要求":
        return "无要求"
    upper = hw_text.upper()
    if re.search(r"GPU|CUDA|VRAM|NVIDIA", upper):
        return "GPU必需"
    if re.search(r"CPU|CORE", upper):
        return "CPU为主"
    if re.search(r"RAM|MEMORY|STORAGE|DISK", upper):
        return "仅内存存储"
    return "其他硬件需求"
```

### 报告模板

报告结构：
- 标题：`# Bittensor 子网综合报告`
- 概览段
- 总览表（Markdown table）
- 有硬件要求的子网详表
- 分类统计

## Boundary Conditions

1. briefings 目录不存在：报错退出
2. MD 文件格式不标准：用默认值填充，不崩溃
3. 文件名不符合 `SN{id}_{name}.md` 格式：跳过
4. 空文件或缺少某段：has_hw=False，hw_text="无要求"

## CLI Arguments

- `--input-dir`：briefings 目录路径，默认 `briefings/`（与脚本同目录）
- `--output`：输出报告路径，默认 `subnet_report.md`（与脚本同目录）
