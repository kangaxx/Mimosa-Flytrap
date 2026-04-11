# Task Memory Tracking System

本项目使用此目录（`tasks/`）来记录和回查各项任务的生命周期、状态和执行过程。

## 命名与结构规范
每个任务对应一个独立 Markdown 文件，文件命名按以下格式：
`[YYYYMMDD]_[XXXXXX]_[ task_name ].md`

- **YYYYMMDD**: 任务创建时的日期（年月日），例如 `20260411`
- **XXXXXX**: 六位数字的序列号，自 `000001` 开始顺序递增
- **task_name**: 任务主题的英文字符或简要中文拼音描述（可选，推荐英文）

例如：`20260411_000001_setup_task_tracking.md`

## 任务状态 (Status)
- **Pending (待处理)**
- **In Progress (进行中)**
- **Blocked (阻塞)**
- **Completed (已完成)**
- **Canceled (已取消)**

您可以直接复制 `TASK_TEMPLATE.md` 创建新任务。
