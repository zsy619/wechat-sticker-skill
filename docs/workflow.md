# 工作流程与规范

## 核心工作流程

```
用户输入(链接/主题/内容)
    ↓
┌─ 输入类型检测 ─┐
│ 1. URL链接    │ → 获取链接内容 + 联网搜索相关内容
│ 2. 主题词     │ → 联网搜索相关内容
│ 3. 内容文本   │ → 提取核心 + 联网搜索相关内容
└───────────────┘
    ↓
内容聚合分析 (content-analysis.md)
    ↓
贴图设计 Manifest (sticker-manifest.md)
    ↓
生成贴图提示词 (prompts/*.md)
    ↓
图片生成（两段式：AI → Remotion）
    ↓
输出汇总 & 标签推荐
```

## 输入类型检测规则

### 1. URL 链接

- **检测规则**：输入以 `http://` 或 `https://` 开头
- **处理流程**：
  1. 使用 `baoyu-url-to-markdown` 获取链接内容
  2. 提取核心主题（标题、首段内容）
  3. 联网搜索相关内容

### 2. 主题词

- **检测规则**：短文本（≤15字符），不包含URL模式
- **处理流程**：
  1. 直接使用主题作为搜索关键词
  2. 联网搜索相关内容

### 3. 内容文本

- **检测规则**：长文本（>15字符），不包含URL模式
- **处理流程**：
  1. 提取核心内容和关键词
  2. 联网搜索相关趋势和热点

## 联网搜索策略

### 搜索关键词构建

- 主题 + "微信贴图"
- 主题 + "表情包"
- 主题 + "Emoji"
- 主题 + "热点"

### 内容提取重点

- 核心功能和特点
- 独特卖点（USP）
- 目标用户群体
- 使用场景

## 项目命名规则

### Topic Slug 生成规则

- 全部小写
- 特殊字符转换为连字符
- 空格用连字符替换
- 超过30字符截断

### 目录冲突解决规则

- 首次创建：`~/wechat-stickers/{topic-slug}/`
- 冲突时：`~/wechat-stickers/{topic-slug}-YYYYMMDD-HHMMSS/`

## 项目目录结构

详见 [project-structure.md](project-structure.md)。


---

## Session Log 记录规范 {#session-log-记录规范}

每次生成贴图包**自动生成** `session-log.md`（项目根目录），由 `scripts/generate_session_log.py` 在工作流末尾执行（`--with-session-log`，默认开启）。

### 必须记录的字段

| 字段 | 说明 |
|------|------|
| 模型 | 如 `minimax/MiniMax-M2.7` |
| 输入 Token | 各阶段输入之和 |
| 输出 Token | 各阶段输出之和 |
| 总 Token | 输入 + 输出 |
| 处理时长 | 秒 |
| 估算费用 | 约 ¥N |

### 估算公式

```
费用 = (输入tokens + 输出tokens) / 1,000,000 × 单价（元/1M tokens）
```

### 手动补充 Token

生成完成后，通过 `session_status` 命令查看当次 Token 消耗，手动填入 `session-log.md` 的 Token 消耗记录表，便于项目复盘和成本优化。

### 示例

```
| 阶段 | 输入 | 输出 | 合计 |
|------|------|------|------|
| 内容聚合分析 | 1,200 | 380 | 1,580 |
| sticker-manifest | 420 | 290 | 710 |
| prompts × 6 | 6,840 | 2,160 | 9,000 |
| **总计** | **8,460** | **2,830** | **11,290** |
```

## Tags 标签记录规范 {#tags-标签记录规范}

每次生成贴图包**自动生成** `tags.md`（项目根目录），由 `scripts/generate_tags.py` 在工作流步骤 5.5 执行（`--with-tags`，默认开启）。

### 功能

- 从 manifest 或 prompts 目录提取关键词和贴图数量
- 按主题匹配 + 关键词命中 + 类别加成三轮打分
- 输出 20 个推荐标签（按热度排序）

### 参数

| 参数 | 说明 |
|------|------|
| `--input` | `sticker-manifest.md` 路径或 `prompts/` 目录 |
| `--output` | `tags.md` 输出路径 |
| `--theme` | 主题（manifest 未指定时使用） |

### 标签类别

| 类别 | 示例 |
|------|------|
| positive | 开心、加油、点赞、可爱、治愈 |
| negative | 难过、崩溃、无语、焦虑、疲惫 |
| reactions | 哈哈、笑死、666、绝了、打工人 |
| social | 职场、开会、学习、摸鱼、躺平 |
| tech | 程序员、代码、AI、效率、工具 |
| lifestyle | 美食、咖啡、熬夜、健身、旅行 |
| trending | 干饭人、尾款人、内卷、绝绝子 |

### 示例

```bash
python3 scripts/generate_tags.py \
    --input sticker-manifest.md \
    --output tags.md \
    --theme neon
```

## Remotion 分段渲染（超长视频处理）

Remotion 在 frame 2500-3000 时 Chrome headless 可能崩溃。如需渲染超长内容（>60秒）：

1. **分段渲染**：每段 30 秒，分别导出后用 ffmpeg 拼接
2. **简化动画**：减少每帧动画元素数量，用 CSS 渐变替代动画 SVG
3. **指定系统 Chrome**：避免 SSL 证书问题（详见 [qa.md](qa.md#remotion-已知问题)）
