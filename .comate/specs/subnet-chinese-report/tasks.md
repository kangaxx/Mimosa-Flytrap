# Bittensor Subnet 中文综合报告生成器 - Task Plan

- [x] Task 1: 搭建脚本骨架与 MD 解析
    - 1.1: 创建 `generate_subnet_report.py`，编写 argparse CLI（--input-dir, --output）
    - 1.2: 实现 `parse_briefing()` 从单个 MD 文件提取子网ID、名称、Git项目、硬件要求
    - 1.3: 实现 `load_all_briefings()` 遍历目录解析所有 MD 文件，按子网ID排序

- [x] Task 2: 实现分类与统计逻辑
    - 2.1: 实现 `classify_hw()` 根据硬件要求内容分类（GPU必需/CPU为主/仅内存存储/其他硬件需求/无要求）
    - 2.2: 实现统计汇总函数，计算总数、有/无硬件要求数、各分类数量

- [x] Task 3: 实现中文报告渲染与输出
    - 3.1: 实现概览段渲染（总数、有GitHub数、有/无硬件要求数）
    - 3.2: 实现子网总览表渲染（Markdown table，按ID排序）
    - 3.3: 实现有硬件要求子网详表渲染（含硬件要求摘要前100字）
    - 3.4: 实现分类统计段渲染
    - 3.5: 串联 main() 流程，运行并验证输出
