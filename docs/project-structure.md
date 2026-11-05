# 项目目录结构

本文档描述贴图生成项目的完整目录结构。

```
~/wechat-stickers/{项目根目录}/                              ← 用户项目目录
│
├── prompts/                             ← 贴图提示词源文件（输入）
│   ├── 01-贴图1.md
│   └── 02-贴图2.md
│
├── remotion-sticker/      ← 阶段二 Remotion 项目（每张贴图一个帧）
│   ├── package.json                     ← @remotion/cli 4.0.448, remotion 4.0.448
│   └── src/
│       ├── index.tsx                    ← registerRoot 入口
│       ├── StickerComponent.tsx          ← 外层组件（返回 <Composition>）
│       ├── StickerContent.tsx           ← 内层组件（含 useCurrentFrame + 动画）
│       └── styles.css
│
├── assets/                              ← 非指定风格输出（GIF+PNG，可选）
├── assets-cyberpunk/                    ← cyberpunk：同序号 .gif + .png
├── assets-kawaii/                       ← kawaii：同序号 .gif + .png
├── assets-neon/                         ← neon：同序号 .gif + .png
├── assets-retro/                        ← retro：同序号 .gif + .png
├── assets-hand-drawn/                   ← hand-drawn：同序号 .gif + .png
├── assets-minimal/                      ← minimal：同序号 .gif + .png
├── assets-meme/                         ← meme：同序号 .gif + .png
│
├── content-analysis.md                  ← 内容聚合分析文档
├── sticker-manifest.md                  ← 贴图设计清单
└── stickers.zip                        ← 最终打包（可选）
```


## 目录说明

| 目录 | 说明 |
|------|------|
| `prompts/` | 输入的贴图提示词 Markdown 文件 |
| `remotion-sticker/` | Remotion 渲染项目（隐藏目录，生成后保留） |
| `assets-{theme}/` | 各风格输出目录（每张贴图同时有 `.gif` 与 `.png`） |
| `content-analysis.md` | 内容聚合分析文档 |
| `sticker-manifest.md` | 贴图设计清单 |
| `stickers.zip` | 打包后的微信贴图（可选） |

## 生成流程中的目录变化

```
创建项目
    ↓
prompts/ 已有（用户输入或 AI 生成）
    ↓ 阶段一
content-analysis.md + sticker-manifest.md（内容聚合）
    ↓ 阶段二
remotion-sticker/（Remotion 项目）
    ↓
assets-{theme}/（GIF + PNG 双格式）
    ↓
stickers.zip（打包）
```
