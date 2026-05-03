# Subnet GitHub Briefing Generator - Task Plan

- [x] Task 1: 搭建脚本骨架与 CSV 读取
    - 1.1: 创建 `generate_subnet_briefings.py`，编写 argparse CLI 参数解析（--input, --output-dir, --timeout, --delay, --no-api）
    - 1.2: 实现 CSV 读取函数 `load_subnet_csv()`，过滤 github_links 为空的行
    - 1.3: 实现 main() 入口，串联读取流程，打印基本信息

- [x] Task 2: 实现 GitHub URL 规范化
    - 2.1: 实现 `normalize_github_url()`，从 URL 提取 owner/repo，处理 .git 后缀、/tree/... 路径等
    - 2.2: 处理非仓库 URL（orgs/...）返回 None 并打印警告

- [x] Task 3: 实现 README 获取
    - 3.1: 实现 `fetch_readme_api()` 通过 GitHub API 获取 README（base64 解码）
    - 3.2: 实现 `fetch_readme_raw()` 作为回退，尝试 raw.githubusercontent.com 的 main/master 分支
    - 3.3: 实现 `fetch_readme()` 整合两种方式，处理 404/403/超时等异常

- [x] Task 4: 实现硬件要求提取
    - 4.1: 定义硬件关键词正则 `HW_KEYWORDS`
    - 4.2: 实现 `extract_hardware_requirements()`，按段落粒度匹配含关键词的文本块
    - 4.3: 未匹配到时返回"无要求"

- [x] Task 5: 实现 MD 简报生成与输出
    - 5.1: 实现 `render_briefing_md()` 生成 MD 内容（子网名称、Git 项目名称及链接、硬件要求）
    - 5.2: 实现 `write_briefing()` 写入文件，文件名 `SN{id}_{name}.md`，特殊字符替换为 `_`
    - 5.3: 创建输出目录（如不存在）

- [x] Task 6: 串联主流程与测试运行
    - 6.1: 在 main() 中串联完整流程：CSV 读取 → URL 规范化 → README 获取 → 硬件提取 → MD 生成
    - 6.2: 加入请求间隔 delay 逻辑避免 API 限流
    - 6.3: 用 py311 环境运行脚本，验证输出目录和 MD 文件生成
