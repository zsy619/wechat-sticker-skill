# 最终输出与发布

## 双格式交付（用户定稿）

流水线**同时产出并保留 GIF 与 PNG**，不得二选一、不得删掉任一格式。

| 平台 | 推送素材 | 标题 | 说明 |
|------|----------|------|------|
| 贴图推送 / 微信公众号 | **优先 GIF** | ≤20 字 | 团队：贴图推送一律推 GIF；GIF → 公众号 |
| 抖音 / 小红书 | **PNG** | ≤20 字 | 静图适配短视频/图文；PNG 成品必须保留 |
| 微信贴图包 ZIP | GIF + PNG 均可入包 | — | 默认打包保留两种；可用 `--gif-only` / `--png-only` 临时筛选，**交付目录仍须两种都在** |

详见 [project-structure.md](project-structure.md)。

- **尺寸**：1080×1440px（微信贴图标准）
- **格式**：每张贴图交付 `{num}-{name}.gif` **与** `{num}-{name}.png`（同序号同名）
- **命名**：`{序号}-{贴图名称}.png` 与 `.gif`

### AI / Remotion 与双格式

- **AI 出图**：优先产出 PNG 静图 → 视为中间帧/静图成品；**必须再导出同名 GIF**（可用 Remotion 动画或 ffmpeg 从序列帧合成），且 **PNG 成品保留**给抖音/小红书。
- **Remotion**：默认 render 出 GIF；另导出一帧 Still 为同名 PNG（或保留 AI PNG），两边产物都留在 `assets-{theme}/`。

### ZIP 打包

优先用脚本（保留双格式）：

```bash
python3 scripts/pack_stickers.py \
  --input assets-{theme}/ \
  --output stickers-{theme}.zip
```

临时只要一种时可用 `--gif-only` / `--png-only`，**不改变** `assets-{theme}/` 里已有的双格式文件。

### 输出汇总格式

```
═══════════════════════════════════════════
    微信贴图生成完成！
═══════════════════════════════════════════

主题: {topic}
生成方式: AI / Remotion
风格: {theme}
贴图数量: {N} 张（各含 GIF + PNG）
输出目录: ~/wechat-stickers/{slug}/assets-{theme}/

标签推荐:
  #微信表情 #微信贴图 #AI工具 #科技感 #赛博朋克
```

## 多平台发布规格

### 图片规格表

| 类型 | 尺寸 | 宽高比 | 文件大小 | 格式 | 用途 |
|------|------|--------|---------|------|------|
| 贴图（公众号/贴图推送） | 1080×1440px | 3:4 | ≤2MB | **GIF** | 公众号正文 / 贴图推送（默认） |
| 贴图（抖音/小红书） | 1080×1440px | 3:4 | ≤2MB | **PNG** | 短视频/图文静图，标题 ≤20 字 |
| 封面 | 900×383px | 9:4 | ≤500KB | PNG | 公众号封面 |
| 缩略图 | 200×267px | 3:4 | ≤100KB | PNG | 文末汇总 |

### 草稿箱与定时（团队规则）

- 文案与素材**只进草稿箱**，不直接对外发布。
- 无特别说明时，定时发布窗口为 **19:00–22:00（Asia/Shanghai）**。
- 用户明确说「立即发」才立即发布；否则一律按上述窗口定时。
- `generate_post.py` / `post.md` 生成的是草稿文案，不是已发布状态。

### 封面 / 缩略图（可选）

需要缩放时用 `scripts/pack_stickers.py --cover/--thumbnail`（见下方），或查 `pack_stickers.py --help`；不手写平行 ffmpeg 流程。

### 公众号排版建议

1. **封面图**：使用 `cover-*.png`，突出主题和风格
2. **正文贴图**：优先插入同序号 **GIF**；PNG 留给抖音/小红书分发
3. **缩略图**：用于文末汇总展示，格式统一
4. **标题**：≤20 字（与抖音/小红书一致）

## 平台文案分支

| 平台 | 素材 | 文案产物 | 标题 |
|------|------|----------|------|
| 公众号 | GIF | `post.md`（`--platform wechat`，默认） | ≤20 字 |
| 抖音 / 小红书 | PNG | `post-douyin.md` / `post-xhs.md`（`--platform douyin|xhs`） | ≤20 字 |

模板与字段见 [references/copy-template.md](../references/copy-template.md)；命令见 [cli.md](cli.md)。

## 标签推荐策略

自动生成 5-10 个相关标签：

| 类别 | 标签 |
|------|------|
| 平台标签 | #微信表情 #微信贴图 #WeChatStickers |
| 情感标签 | #可爱 #搞笑 #治愈 #社恐自救 #打工人 #摸鱼 |
| 主题标签 | 根据内容自动提取（如 #AI #编程 #职场 #生活） |

---

## 自动化打包

使用 `scripts/pack_stickers.py` 自动打包并生成封面/缩略图：

```bash
# 打包（默认保留 assets 内 GIF+PNG）+ 生成封面 + 生成缩略图
python3 scripts/pack_stickers.py \
  --input assets-cyberpunk/ \
  --output stickers-cyberpunk.zip \
  --cover 900x383 \
  --thumbnail 200x267

# 仅打包
python3 scripts/pack_stickers.py \
  --input assets-cyberpunk/ \
  --output stickers-cyberpunk.zip
```

**输出内容**：
- `stickers-cyberpunk.zip` — 贴图打包（目录内 GIF 与 PNG 均保留；临时筛选用 `--gif-only` / `--png-only`）
- `cover-900x383.png` — 公众号封面（可选）
- `thumbnail-200x267.png` — 文末缩略图（可选）
- `tags.md`（项目根目录）— 标签推荐文档（**自动生成**，由 `generate_tags.py` 在步骤 5.5 生成）

### 标签生成

`tags.md`（项目根目录）由 `run_full_pipeline.py` 步骤 5.5 自动生成（`--with-tags`，默认开启），无需手动执行。

独立使用：
```bash
python3 scripts/generate_tags.py \
  --input sticker-manifest.md \
  --output tags.md
```
