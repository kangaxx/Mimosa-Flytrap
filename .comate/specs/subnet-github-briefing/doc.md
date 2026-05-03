# Subnet GitHub Briefing Generator

## Requirement

开发一个 Python 脚本 `generate_subnet_briefings.py`，读取 `result.csv`（由 `scrape_tao_subnet_githubs.py` 生成），遍历每个 GitHub 仓库地址，获取项目的 README 文档，提取关键信息并生成简报 MD 文件。

## Input

- `result.csv`，字段：`subnet_id`, `subnet_name`, `subnet_url`, `github_links`
  - `github_links` 可能为空（无 GitHub 的子网跳过）
  - `github_links` 中可能包含非标准仓库 URL（如 `https://github.com/orgs/...`、带 `.git` 后缀、带 `/tree/main` 后缀）

## Output

- 输出目录 `briefings/`（与脚本同目录），每个有 GitHub 链接的子网生成一个 MD 文件
- 文件命名：`SN{subnet_id}_{subnet_name}.md`（subnet_name 中的特殊字符替换为 `_`）
- MD 文件内容：
  - 子网名称
  - Git 项目名称（从 GitHub URL 中提取 `owner/repo`）
  - 项目对硬件要求（从 README 中提取；如果没有就写"无要求"）

## Architecture & Technical Approach

1. **读取 CSV**：用 `csv` 标准库读取 `result.csv`，过滤掉 `github_links` 为空的行
2. **GitHub API 获取 README**：使用 GitHub REST API `GET /repos/{owner}/{repo}/readme` 获取 README 内容（base64 解码），避免 HTML 解析；若 API 限流则回退到 raw.githubusercontent.com 直接获取
3. **URL 规范化**：将 GitHub URL 统一为 `owner/repo` 格式
   - 去除 `.git` 后缀、`/tree/...`、`/blob/...` 等路径
   - 处理 `github.com/orgs/...` 等非仓库 URL（标记为无法访问）
4. **硬件要求提取**：在 README 文本中用正则匹配常见硬件要求关键词模式
   - 关键词：`GPU`, `CPU`, `RAM`, `memory`, `storage`, `disk`, `VRAM`, `requirements`, `hardware`, `specs`, `NVIDIA`, `CUDA`
   - 匹配关键词所在段落（以连续文本块或列表项为粒度）
   - 未匹配到则输出"无要求"
5. **生成 MD**：使用模板生成简报文件

## Affected Files

| 文件 | 操作 | 说明 |
|---|---|---|
| `agents/bittensor/generate_subnet_briefings.py` | 新建 | 主脚本 |
| `agents/bittensor/result.csv` | 读取 | 数据源 |
| `agents/bittensor/briefings/` | 新建目录 | 输出目录 |

## Data Flow

```
result.csv → CSV 解析 → URL 规范化 → GitHub API / raw URL 获取 README → base64 解码 → 关键词提取 → MD 模板渲染 → briefings/SN{id}_{name}.md
```

## Implementation Details

### URL 规范化逻辑

```python
def normalize_github_url(url: str) -> tuple[str, str] | None:
    """Return (owner, repo) from a GitHub URL, or None if not a repo URL."""
    # Remove trailing .git
    url = url.rstrip("/").removesuffix(".git")
    # Match patterns like github.com/owner/repo or github.com/owner/repo/tree/main/...
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)(?:/.*)?$", url)
    if m:
        return m.group(1), m.group(2)
    return None  # orgs/... or other non-repo URLs
```

### README 获取逻辑

优先使用 GitHub API（需处理 404/403 限流），回退到 raw URL：

```python
def fetch_readme(session, owner: str, repo: str, timeout: int) -> str | None:
    # Try GitHub API first
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    r = session.get(api_url, timeout=timeout)
    if r.status_code == 200:
        import base64
        data = r.json()
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    # Fallback: try common README filenames via raw URL
    for name in ["README.md", "README.rst", "README.txt", "README"]:
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{name}"
        r = session.get(raw_url, timeout=timeout)
        if r.status_code == 200:
            return r.text
        # Also try master branch
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{name}"
        r = session.get(raw_url, timeout=timeout)
        if r.status_code == 200:
            return r.text
    return None
```

### 硬件要求提取

```python
HW_KEYWORDS = re.compile(
    r"(?i)(?:GPU|CPU|RAM|VRAM|memory|storage|disk|NVIDIA|CUDA|hardware|requirements?|specs|minimum|recommended)"
)

def extract_hardware_requirements(readme_text: str) -> str:
    lines = readme_text.split("\n")
    hw_sections = []
    current_section = []
    in_hw_section = False

    for line in lines:
        if HW_KEYWORDS.search(line):
            if not in_hw_section:
                in_hw_section = True
                current_section = [line]
            else:
                current_section.append(line)
        elif in_hw_section:
            if line.strip() == "":
                # End of paragraph/block
                hw_sections.append("\n".join(current_section))
                current_section = []
                in_hw_section = False
            else:
                current_section.append(line)

    if current_section:
        hw_sections.append("\n".join(current_section))

    if not hw_sections:
        return "无要求"
    return "\n".join(hw_sections).strip()
```

### MD 模板

```markdown
# {subnet_name}

- **子网名称**: {subnet_name}
- **Git 项目**: [{owner}/{repo}](https://github.com/{owner}/{repo})

## 硬件要求

{hardware_requirements}
```

## Boundary Conditions & Exception Handling

1. **CSV 不存在**：打印错误并退出
2. **GitHub URL 无法规范化**（如 orgs 链接）：跳过并打印警告
3. **README 不存在**（404）：生成简报，硬件要求写"无要求"
4. **GitHub API 限流**（403）：回退到 raw URL 方式
5. **README 内容非 UTF-8**：用 `errors="replace"` 解码
6. **网络超时**：跳过该仓库，打印警告
7. **subnet_name 含特殊字符**（`/`, ` `, `#` 等）：替换为 `_` 用于文件名
8. **重复 GitHub URL**（多个子网指向同一仓库）：各自生成独立简报

## CLI Arguments

- `--input`：CSV 文件路径，默认 `result.csv`（与脚本同目录）
- `--output-dir`：输出目录，默认 `briefings/`（与脚本同目录）
- `--timeout`：HTTP 超时秒数，默认 20
- `--delay`：请求间隔秒数，默认 1.0（避免 API 限流）
- `--no-api`：跳过 GitHub API，直接用 raw URL 获取

## Expected Outcome

运行后 `briefings/` 目录下生成约 104 个 MD 文件（对应有 GitHub 链接的子网），每个文件包含子网名称、项目名称和硬件要求信息。
