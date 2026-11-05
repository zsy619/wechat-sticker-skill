---
name: wechat-sticker-skill
description: Create WeChat emoji sticker series from any input (URL, topic, or content). Use when user asks to "做微信贴图", "微信贴图", "创建微信贴图包", "WeChat stickers", "微信emoji", "根据内容生成贴图", "做一套贴图", "生成贴图". Triggers on sticker creation, emoji design, reaction images, or any WeChat sticker-related request, including "表情包", "公众号贴图", "贴图推送". Bundled scripts/ pipeline (AI → Remotion fallback) outputs 1080×1440 GIF/PNG stickers, ZIP, tags.md and a 公众号 post.md.
version: 4.9.6
tags: ["微信", "贴图", "表情包", "微信表情包", "微信贴图", "帧动画", "图片生成"]
metadata:
  author: zhushuyan
  updated: "2026-05-03"

---

# 微信贴图生成器 v4.9.6 (WeChat Sticker Creator)

本技能根据用户输入（链接、主题或内容），自动进行内容聚合、贴图设计和生成，输出一套完整的微信表情包。

## 开工确认（多步任务第一步）

运行 pipeline 前先回一句："我计划用 `--theme <风格>` 生成约 N 张贴图，输入类型是 URL/主题/文本，图像走 AI（会调用付费接口）→ 失败再走 Remotion，输出到 `~/wechat-stickers/<slug>/`。现在开始吗？"，用户确认后再执行。
用户或调度 bot 已明确给出主题 + 风格（+ 数量）时视为已确认，直接执行。

完成标志：`scripts/qa_check.py` 退出码为 0，且输出图片数 = prompts 数；未达标不交付、不进入打包与推广文档。

## 核心设计：两段式图像生成

```
用户输入(链接/主题/内容)
    ↓
内容聚合分析 → 贴图设计 → 提示词生成
    ↓
┌─ 图像生成（优先级递进） ───────────────────────────────┐
│  ① AI生成图像（首选）                                   │
│     调用大模型（GPT-Image / Seedream 等）直接生成高质量帧
│     ↓ 异常                                              │
│  ② Remotion 帧导出（第二选择）                          │
│     建独立 Remotion 项目，每张贴图对应每帧 = <Composition> 组件
│     导出 **GIF**（90帧动画），独特视觉设计 + 动画特效                              │
│     ↓ 异常                                              │
│  报错停止（不再降级）                                   │
└────────────────────────────────────────────────────────┘
    ↓
最终输出（ZIP / 公众号发布）
```

**优先级**：AI → Remotion。Remotion 失败则报错，不再降级。

## skill 项目结构

```
wechat-sticker-skill/                     ← 技能根目录
├── SKILL.md                              ← 入口文件
├── remotion/template/                    ← index.tsx / StickerComponent.tsx / StickerContent.tsx 模板
├── remotion/styles/base.css             ← 全局 CSS 重置
├── scripts/                              ← 黑盒脚本（只看 --help，不读源码）
│   ├── run_full_pipeline.py              ← 完整工作流入口
│   ├── generate_content_analysis.py / generate_manifest.py / generate_prompts.py
│   ├── generate_frames.py                ← 图片生成（AI → Remotion）
│   ├── pack_stickers.py / qa_check.py    ← 打包 / QA
│   ├── generate_tags.py / generate_session_log.py / generate_post.py
│   └── _vocab.py                         ← 共享词汇表（VOCABULARY + THEMES）
├── docs/                                 ← 参考文档（按下方索引按需读，不复制到项目）
├── references/                           ← copy.md / token-stats 模板
├── evals/                                ← 评测用例
└── demo/ai-coding-assistant/            ← 满分样板项目（仿结构，不抄内容）
```

## 项目目录结构

详见 [docs/project-structure.md](docs/project-structure.md)。

## 快速开始

```bash
# ── 完整工作流（自动化串联）──────────────────────────────
# 一次性完成：内容聚合 → manifest → prompts → 图片生成
python3 scripts/run_full_pipeline.py \
  --input "AI编程助手" \
  --output ~/wechat-stickers/ai-coding-assistant \
  --theme cyberpunk
```

分步执行、`--mode` / `--continue-on-error` / `--dry-run` / `--gif-only` 等参数、补跑命令 → [docs/cli.md](docs/cli.md)。

## 核心概念

### 为什么是 Remotion？

Remotion 作为 React 组件，可以用代码精确控制每一帧的视觉元素，适合需要高质量、独特视觉设计的贴图。

### 两段式降级机制

| 优先级 | 方式 | 优势 | 劣势 |
|--------|------|------|------|
| 1 | AI生成 | 语义理解、真实光影、细节丰富 | API成本、调用失败可能 |
| 2 | Remotion帧导出 | 像素级控制、程序化精确、动画可能 | 需要Node.js环境、帧组件编写 |

Remotion 失败则报错，不再降级。

### Remotion 帧设计原则

每套贴图使用**单一 Remotion 项目 + Sequence 架构**：
- **外层**（StickerComponent）：返回 `<Composition>`，**不使用** `useCurrentFrame()`
- **中层**（StickerContent）：持有 `<Sequence>` 列表，注入 `__SEQUENCES__`
- **内层**（StickerScene）：每张贴图的视觉组件，**使用** `useCurrentFrame()` + 5个动画函数

**输出规格**：1080×1440，90帧@30fps（3秒），**GIF 动画**

详见 [docs/frame-design.md](docs/frame-design.md)。

## 支持的风格

`cyberpunk` / `kawaii` / `neon` / `retro` / `hand-drawn` / `minimal` / `meme`

## 项目文档

> **说明**：`tags.md` / `session-log.md` / `post.md` 由 pipeline **自动生成**（步骤 5.5、7、8），直接输出到项目根目录。技能 `docs/` 目录下的文档为内部参考，不复制到项目。

| 文档 | 生成脚本 | 输出位置 | 说明 |
|------|----------|----------|------|
| `tags.md` | `generate_tags.py` | 项目根目录 | 从 prompts 提取关键词，微信贴图标签 |
| `session-log.md` | `generate_session_log.py` | 项目根目录 | Token 估算、阶段耗时、项目记录 |
| `post.md` | `generate_post.py` | 项目根目录 | 公众号推广文案（从 manifest 提取） |

**自动生成时机**：完整 pipeline（`--mode auto`）中，步骤 5.5/7/8 自动执行。单独运行时需手动调用对应脚本。

## 文档索引（何时读哪份）

| 场景 | 读哪份 |
|---|---|
| 判断输入类型（URL/主题/文本）、命名、目录冲突 | [docs/workflow.md](docs/workflow.md) |
| 写 content-analysis / manifest / prompts | [docs/content-format.md](docs/content-format.md)、[docs/prompts-format.md](docs/prompts-format.md)（>10k 字，按需 grep：`visual_elements`、`词汇表校验`、`自检清单`、`常见错误`） |
| AI 生成失败、provider 切换 | [docs/image-generation.md](docs/image-generation.md) |
| Remotion 组件 / 动画 / 报错 | [docs/frame-design.md](docs/frame-design.md)、[docs/remotion-projects.md](docs/remotion-projects.md)、[docs/qa.md](docs/qa.md)「Remotion 已知问题」 |
| 打包、封面、公众号规格 | [docs/output.md](docs/output.md) |
| 交付前检查 | [docs/qa.md](docs/qa.md) + `scripts/qa_check.py` |
| 写推广文案 copy.md | [references/copy-template.md](references/copy-template.md) |
| 看一套完整产出长什么样 | [demo/ai-coding-assistant/](demo/ai-coding-assistant/) |
| 项目目录 | [docs/project-structure.md](docs/project-structure.md) |
| 命令与参数 | [docs/cli.md](docs/cli.md) |
