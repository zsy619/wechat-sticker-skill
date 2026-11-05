# 贴图 Prompt 生成规范（完整版）

本文档定义 `prompts/{num}-{name}.md` 的完整写法，涵盖 frontmatter 字段规范、正文结构、视觉元素词汇表、主题配色、字体特效描述。

---

## 一、文件命名

```
prompts/
├── 01-{贴图名}.md     ← 格式：序号-中文名
├── 02-{贴图名}.md
└── 03-{贴图名}.md
```

- 序号从 01 开始，不足两位补零
- 文件名只用中文，不含空格和英文（如 `01-画布手写.md`）
- 每个 prompt 文件对应一张贴图

---

## 二、文件结构

```markdown
---
name: {贴图中英文标识}
copy: {核心文案}
visual_elements: [{元素1}, {元素2}, {元素3}]
style_keyword: [{风格词1}, {风格词2}]
theme: {主题键}
---

# {贴图标题}

## 核心文案（必须展示在贴图中）
{核心文案全文}

## 视觉设计规则

### 主体
{主体描述：有什么视觉元素，它们的关系}

### 风格要求
- 主题：{主题描述}
- 主色：{十六进制颜色}（{颜色名}）
- 副色：{十六进制颜色}（{颜色名}）
- 背景：{十六进制颜色}
- 文字：{颜色描述}

### 动画
- {动画效果描述}

### 文字展示
- 核心文案：{核心文案}
- 字体：{字体名}，{字号}px
- 位置：{位置描述}
- 效果：{效果描述}
```

---

## 三、Frontmatter 字段详解

### 3.1 `name` — 贴图标识

| 规则 | 说明 |
|------|------|
| 格式 | 中文，建议2-4字 |
| 用途 | 生成文件名和贴图标题 |
| 示例 | `name: 画布手写` |

### 3.2 `copy` — 核心文案

| 规则 | 说明 |
|------|------|
| 字数 | 建议8-16字（微信文案上限） |
| 语言 | 中文为主 |
| 内容 | 表达贴图的使用场景或情感 |
| 样式 | 短促有力、口语化、适合当表情包文案 |
| 示例 | `copy: 随手一画，AI帮你算` |

**copy 写作原则**：
- ✅ 有画面感（"随手一画"比"开始计算"更有画面）
- ✅ 有情感钩子（"AI帮你算"暗示省力）
- ❌ 不要太正式（"正在进行数学运算"太严肃）
- ❌ 不要超20字（微信限制）
- ❌ 不要纯描述（"这是等号"没有情绪）

**常见 copy 类型**：

| 类型 | 示例 | 适用场景 |
|------|------|---------|
| 动作类 | 随手一画，AI帮你算 | 画布手写 |
| 结果类 | AI一画答案就出来咯 | AI计算 |
| 等待类 | 写完等号等答案出来 | 等号求解 |
| 感叹类 | Apple看了也说绝 | MathNotes |
| 情绪类 | 不对不对全部清掉 | 清空重写 |
| 确认类 | AI算出答案是八没错 | 答案揭晓 |

### 3.3 `visual_elements` — 视觉元素列表

| 规则 | 说明 |
|------|------|
| 格式 | `[元素1, 元素2, 元素3]`（逗号分隔，**不用引号**） |
| 数量 | 推荐3个元素（太少无层次，太多显拥挤） |
| 键值 | **必须**使用 emoji 词汇表中的英文 key |
| 顺序 | 从左到右对应贴图中从左到右的 emoji 排列 |

**标准词汇表**：

| key（前端 yaml 写这个） | emoji | 含义 |
|----------------------|-------|------|
| `brain` | 🧠 | AI 大脑 / 神经网络 |
| `neural_network` | 🧠 | 神经网络节点 |
| `terminal` | 💻 | 终端窗口 |
| `math_canvas` | 📐 | 数学画布 |
| `equals_sign` | ＝ | 等号（全角，避免 JSX 冲突） |
| `question_mark` | ？ | 问号（全角） |
| `ai_chip` | 🤖 | AI 芯片 |
| `eraser` | 🧹 | 橡皮擦 |
| `checkmark` | ✓ | 对勾 |
| `lightning` | ⚡ | 闪电 |
| `heart` | ❤ | 红心 |
| `spotlight` | 🔦 | 光晕 |
| `network_node` | 🔗 | 网络节点 |
| `button` | 🔘 | 按钮 |
| `robot` | 🤖 | 机器人 |
| `code` | 💻 | 代码 |
| `algorithm` | 🔣 | 算法 |
| `cpu` | 🖥️ | 处理器 |
| `server` | 🗄️ | 服务器 |
| `database` | 🗃️ | 数据库 |
| `cloud` | ☁️ | 云 |
| `data` | 📊 | 数据 |
| `function` | ƒ | 函数 |
| `variable` | x | 变量 |
| `debug` | 🐛 | 调试 |
| `deploy` | 🚀 | 部署 |
| `star` | ⭐ | 星星 |
| `fire` | 🔥 | 火 / 热门 |
| `hundred` | 💯 | 100 分 |
| `thumbs_up` | 👍 | 点赞 |
| `clap` | 👏 | 鼓掌 |
| `pray` | 🙏 | 祈祷 / 感谢 |
| `muscle` | 💪 | 加油 |
| `thinking` | 🤔 | 思考 |
| `eyes` | 👀 | 围观 |
| `trophy` | 🏆 | 奖杯 |
| `medal` | 🏅 | 奖牌 |
| `crown` | 👑 | 王冠 |
| `rocket` | 🚀 | 火箭 |
| `alarm` | ⏰ | 闹钟 |
| `bell` | 🔔 | 铃铛 |
| `megaphone` | 📢 | 广播 |
| `wrench` | 🔧 | 扳手 |
| `hammer` | 🔨 | 锤子 |
| `scissors` | ✂️ | 剪刀 |
| `pencil` | ✏️ | 铅笔 |
| `book` | 📖 | 书本 |
| `lightbulb` | 💡 | 灯泡 / 灵感 |
| `envelope` | ✉️ | 信封 |
| `gift` | 🎁 | 礼物 |
| `tada` | 🎉 | 庆祝 |
| `balloon` | 🎈 | 气球 |
| `confetti` | 🎊 | 彩带 |
| `music` | 🎵 | 音乐 |
| `headphones` | 🎧 | 耳机 |
| `camera` | 📷 | 相机 |
| `phone` | 📱 | 手机 |
| `coffee` | ☕ | 咖啡 |
| `pizza` | 🍕 | 披萨 |
| `rice` | 🍚 | 米饭 |
| `fruit` | 🍎 | 水果 |
| `cake` | 🎂 | 蛋糕 |
| `cookie` | 🍪 | 饼干 |
| `bread` | 🍞 | 面包 |
| `beer` | 🍺 | 啤酒 |
| `cocktail` | 🍸 | 鸡尾酒 |
| `wine` | 🍷 | 葡萄酒 |
| `tea` | 🍵 | 茶 |
| `sleeping` | 😴 | 睡觉 |
| `cry` | 😭 | 哭 |
| `laugh` | 😂 | 大笑 |
| `angry` | 😡 | 生气 |
| `cool` | 😎 | 酷 |
| `shy` | 😳 | 害羞 |
| `love_letter` | 💌 | 情书 |
| `money` | 💰 | 钱 |
| `gem` | 💎 | 宝石 |
| `warning` | ⚠️ | 警告 |
| `no_entry` | ⛔ | 禁止 |
| `busy` | 🉐 | 忙 |
| `free` | 🆓 | 免费 |
| `secret` | 🤫 | 秘密 |
| `goal` | 🎯 | 目标 |
| `puzzle` | 🧩 | 拼图 |
| `map` | 🗺️ | 地图 |
| `compass` | 🧭 | 指南针 |
| `earth` | 🌏 | 地球 |
| `moon` | 🌙 | 月亮 |
| `sun` | ☀️ | 太阳 |
| `rainbow` | 🌈 | 彩虹 |
| `snowflake` | ❄️ | 雪花 |
| `wave` | 🌊 | 海浪 |
| `anchor` | ⚓ | 锚 |
| `airplane` | ✈️ | 飞机 |
| `car` | 🚗 | 汽车 |
| `bicycle` | 🚲 | 自行车 |
| `clock` | ⏱️ | 计时器 |
| `hourglass` | ⏳ | 沙漏 |
| `calendar` | 📅 | 日历 |
| `key` | 🔑 | 钥匙 |
| `lock` | 🔒 | 锁 |
| `bulb` | 💡 | 灯泡 |
| `flag` | 🚩 | 旗帜 |
| `microphone` | 🎤 | 麦克风 |
| `video` | 🎬 | 视频 |
| `tv` | 📺 | 电视 |
| `clipboard` | 📋 | 剪贴板 |
| `chart` | 📈 | 图表 |
| `pen` | 🖊️ | 笔 |
| `ruler` | 📏 | 直尺 |
| `paperclip` | 📎 | 回形针 |
| `stamp` | 📮 | 邮票 |
| `inbox` | 📥 | 收件箱 |
| `outbox` | 📤 | 发件箱 |
| `folder` | 📁 | 文件夹 |
| `file` | 📄 | 文件 |
| `link` | 🔗 | 链接 |
| `email` | 📧 | 邮件 |
| `call` | 📞 | 电话 |
| `sound` | 🔊 | 声音 |
| `mute` | 🔇 | 静音 |
| `vibration` | 📳 | 振动 |
| `eye` | 👁️ | 眼睛 |
| `ear` | 👂 | 耳朵 |
| `nose` | 👃 | 鼻子 |
| `footprints` | 👣 | 脚印 |
| `bone` | 🦴 | 骨头 |
| `microbe` | 🦠 | 微生物 |
| `pill` | 💊 | 药 |
| `syringe` | 💉 | 注射 |
| `thermometer` | 🌡️ | 体温计 |
| `zap` | ⚡ | 电击 |
| `magnet` | 🧲 | 磁铁 |
| `gear` | ⚙️ | 齿轮 |
| `atom` | ⚛️ | 原子 |
| `dna` | 🧬 | DNA |
| `biohazard` | ☣️ | 生物危害 |
| `radioactive` | ☢️ | 辐射 |
| `bio` | 🌱 | 生态 |
| `four_leaf` | 🍀 | 四叶草 |
| `maple` | 🍁 | 枫叶 |
| `cherry` | 🌸 | 樱花 |
| `tulip` | 🌷 | 郁金香 |
| `rose` | 🌹 | 玫瑰 |
| `hibiscus` | 🌺 | 木芙蓉 |
| `shell` | 🐚 | 贝壳 |
| `feather` | 🪶 | 羽毛 |
| `sparkle` | ✨ | 闪光 |
| `diamond` | 💠 | 钻石 |
| `fleur` | ⚜️ | 百合 |
| `comet` | ☄️ | 彗星 |
| `satellite` | 🛰️ | 卫星 |
| `telescope` | 🔭 | 望远镜 |
| `microscope` | 🔬 | 显微镜 |

**❌ 常见错误**（会导致 emoji 不显示）：
```yaml
# ❌ 错误：中文词不在词汇表中
visual_elements: [黑色画布, 白色手写笔迹, 数学公式]

# ✅ 正确：使用英文 key
visual_elements: [math_canvas, brain, equals_sign]
```

**元素组合原则**：
- 第一个元素：视觉焦点（如 `brain` 最常见作为主视觉）
- 最后一个元素：收尾（如 `checkmark` 表示完成感）
- 中间元素：辅助说明（如 `question_mark` 增加等待感）

### 3.4 `style_keyword` — 风格关键词

| 规则 | 说明 |
|------|------|
| 格式 | `[{风格词1}, {风格词2}]` |
| 作用 | 传给 AI 图像生成 API（用于 AI 生成模式） |
| 数量 | 2-3个词 |
| 常用词 | cyberpunk / neon / kawaii / retro / hand-drawn / minimal / meme |

### 3.5 `theme` — 主题键

| 规则 | 说明 |
|------|------|
| 格式 | 对应 THEMES 对象中的 key |
| 值域 | `cyberpunk` / `kawaii` / `neon` / `retro` / `hand-drawn` / `minimal` / `meme` |
| 作用 | 决定配色方案、字体发光颜色 |

**各主题配色**：

| theme | primary | secondary | bg | text |
|-------|---------|-----------|----|------|
| cyberpunk | #00FFFF | #FF00FF | #0D0D1A | #FFFFFF |
| kawaii | #FF69B4 | #FFB6C1 | #FFF0F5 | #4A4A4A |
| neon | #FF00FF | #00FFFF | #1A0033 | #FFFFFF |
| retro | #FFD700 | #FF6B35 | #2D1B00 | #FFFFFF |
| hand-drawn | #8B4513 | #DEB887 | #FFF8DC | #4A4A4A |
| minimal | #333333 | #666666 | #FFFFFF | #333333 |
| meme | #FFFF00 | #FF6600 | #000000 | #FFFFFF |

---

## 四、正文结构详解

### 4.1 标题行

```
# {num}-{贴图名}
```

如 `# 01-画布手写`，与文件名保持一致。

### 4.2 核心文案节

```markdown
## 核心文案（必须展示在贴图中）
随手一画，AI帮你算
```

- 必须包含完整核心文案，与 frontmatter 的 `copy` 字段一致
- 用于 body 展示（优先级高于 frontmatter）

### 4.3 主体描述

```markdown
### 主体
深色背景 + 居中显示 📐画布 + 🧠AI大脑 + ＝等号符号
三元素横向排列，霓虹发光滤镜，底部140px白色文案居中
```

**描述要素**：
1. **背景**（颜色/效果）
2. **主体元素**（emoji + 排列方式）
3. **光效/滤镜**
4. **文案位置**

### 4.4 风格要求

```markdown
### 风格要求
- 主题：cyberpunk / tech-modern
- 主色：#00FFFF（霓虹青）
- 副色：#FF00FF（品红）
- 背景：深色 #0D0D1A
- 文字：白色，底部居中
```

### 4.5 动画描述

```markdown
### 动画
- 呼吸发光：opacity 0.4→1 脉冲
- 脉冲缩放：scale 1→1.06→1
- 浮空动效：translateY 浮起
```

**可描述的动画维度**：
- `opacity`：明暗呼吸
- `scale`：缩放脉冲
- `translateY`：上下浮动
- `filter`：发光/模糊变化
- `textShadow`：霓虹扩散

### 4.6 文字展示

```markdown
### 文字展示
- 核心文案：随手一画，AI帮你算
- 字体：PingFang SC，140px
- 位置：画布底部居中
- 效果：霓虹发光 text-shadow 多层青色
```

---

## 五、完整示例

### 示例一：画布手写

```markdown
---
name: 画布手写
copy: 随手一画，AI帮你算
visual_elements: [math_canvas, brain, equals_sign]
style_keyword: [cyberpunk, neon, tech-modern]
theme: cyberpunk
---

# 01-画布手写

## 核心文案（必须展示在贴图中）
随手一画，AI帮你算

## 视觉设计规则

### 主体
深色背景 + 居中显示 📐画布 + 🧠AI大脑 + ＝等号符号
三元素横向排列，霓虹发光滤镜，底部140px白色文案居中

### 风格要求
- 主题：cyberpunk / tech-modern
- 主色：#00FFFF（霓虹青）
- 副色：#FF00FF（品红）
- 背景：深色 #0D0D1A
- 文字：白色，底部居中

### 动画
- 呼吸发光：opacity 0.4→1 脉冲
- 脉冲缩放：scale 1→1.06→1
- 浮空动效：translateY 浮起

### 文字展示
- 核心文案：随手一画，AI帮你算
- 字体：PingFang SC，140px
- 位置：画布底部居中
- 效果：霓虹发光 text-shadow 多层青色
```

### 示例二：答案揭晓

```markdown
---
name: 答案揭晓
copy: AI算出答案是八没错
visual_elements: [equals_sign, brain, checkmark]
style_keyword: [cyberpunk, neon, success]
theme: cyberpunk
---

# 06-答案揭晓

## 核心文案（必须展示在贴图中）
AI算出答案是八没错

## 视觉设计规则

### 主体
深色背景 + 居中显示 ＝等号 + 🧠AI + ✓对勾
三元素横向排列，青色+橙色双重发光，底部140px白色文案居中

### 风格要求
- 主题：cyberpunk / tech-modern
- 主色：#FF8C00（橙色答案）
- 副色：#00FFFF（霓虹青）
- 背景：深色 #0D0D1A
- 文字：白色，底部居中

### 动画
- 呼吸发光：opacity 0.4→1 脉冲
- 脉冲缩放：scale 1→1.06→1
- 浮空动效：translateY 浮起

### 文字展示
- 核心文案：AI算出答案是八没错
- 字体：PingFang SC，140px
- 位置：画布底部居中
- 效果：霓虹发光 text-shadow 多层橙色
```

---

## 六、自检清单

生成每个 prompt 后，按以下清单逐项检查：

- [ ] `name`：中文，2-4字
- [ ] `copy`：8-16字，口语化，有画面感
- [ ] `visual_elements`：3个，使用英文 key，不含中文词
- [ ] `visual_elements` 的 key 都在词汇表中
- [ ] `theme`：必须是7个主题键之一
- [ ] frontmatter 后有 `---` 闭合行
- [ ] body 中有 `## 核心文案` 节
- [ ] body 中有 `## 视觉设计规则` 节
- [ ] 主体描述包含：背景 + 元素 + 位置
- [ ] 风格要求标注主色/副色/背景色
- [ ] 动画描述列出具体参数
- [ ] 文字展示标注字号≥120px（竖屏大字）

---

## 七、常见错误汇总

| 错误类型 | 错误写法 | 正确写法 |
|---------|---------|---------|
| visual_elements 含中文 | `[黑色画布, AI大脑]` | `[math_canvas, brain]` |
| visual_elements 用了 `=` | `[brain, =, question]` | `[brain, equals_sign, question_mark]` |
| copy 太长 | `copy: 这个数学公式计算结果是八` | `copy: AI算出答案是八没错` |
| copy 缺情绪 | `copy: 计算结果为8` | `copy: AI算出答案是八没错` |
| theme 拼写错误 | `theme: cyberpunk` | `theme: cyberpunk` |
| 元素数量过多 | `[brain, brain, brain, brain]` | `[brain, brain, brain]` |
| 缺少闭合 `---` | 无 | frontmatter 末行 `---` |
| emoji 不在词汇表 | `[robot, computer]` | `[ai_chip, terminal]` |


---

## 八、Session Log 关联记录

每个项目根目录的 `session-log.md` 记录 Token 消耗，prompt 本身不需要写 token 信息。

**模板示例**（见 [session-log.md 模板](../workflow.md#session-log-记录规范)）：

| 阶段 | 输入 | 输出 | 合计 |
|------|------|------|------|
| 内容聚合分析 | N | N | N |
| sticker-manifest | N | N | N |
| prompts × N | N | N | N |
| **总计** | **N** | **N** | **N** |

---

## 九、从 manifest 生成 prompts

每张贴图的 `prompts/*.md` 由 `scripts/generate_prompts.py` 基于 `sticker-manifest.md` 自动生成。

**前置条件**：
- 已存在 `sticker-manifest.md`（由 `scripts/generate_manifest.py` 生成）
- manifest 中 `visual_elements` 字段使用英文 key

**生成命令**：
```bash
python3 scripts/generate_prompts.py \
  --input sticker-manifest.md \
  --output prompts/
```

**自动填充内容**：
- `name`：继承 manifest 的贴图名称
- `copy`：继承 manifest 的核心文案
- `visual_elements`：直接复制 manifest 的英文 key 列表
- `style_keyword`：继承 manifest 的风格词
- `theme`：继承 manifest 的主题键
- 正文：自动基于 theme 配色填充"风格要求"节

---

## 十、visual_elements 词汇表校验规则

所有 `visual_elements` 中的 key **必须**在以下词汇表范围内。校验由 `scripts/qa_check.py` 自动执行。

**完整词汇表**（prompts-format.md 第五节）共 80+ 条，分类：

| 分类 | 代表 key |
|------|---------|
| 核心 AI/技术 | `brain`, `neural_network`, `terminal`, `lightning`, `ai_chip`, `spotlight`, `network_node`, `button`, `code`, `algorithm`, `function`, `variable`, `debug`, `deploy` |
| 情感/反应 | `heart`, `thumbs_up`, `clap`, `pray`, `muscle`, `thinking`, `eyes`, `trophy`, `medal`, `crown`, `star`, `fire`, `hundred`, `laugh`, `cry`, `angry`, `cool`, `shy`, `sleeping` |
| 物品/工具 | `rocket`, `alarm`, `bell`, `megaphone`, `wrench`, `hammer`, `scissors`, `pencil`, `book`, `lightbulb`, `envelope`, `gift`, `tada`, `balloon`, `confetti` |
| 食物/饮料 | `coffee`, `tea`, `beer`, `cocktail`, `wine`, `pizza`, `rice`, `fruit`, `cake`, `cookie`, `bread` |
| 办公/效率 | `phone`, `camera`, `clipboard`, `chart`, `calendar`, `key`, `lock`, `folder`, `file`, `email`, `call`, `microphone`, `video`, `tv`, `clock`, `hourglass`, `pen`, `ruler`, `paperclip`, `stamp`, `inbox`, `outbox` |
| 自然/科学 | `earth`, `moon`, `sun`, `rainbow`, `snowflake`, `wave`, `anchor`, `airplane`, `car`, `bicycle`, `map`, `compass`, `flag`, `satellite`, `telescope`, `microscope` |
| 心情/状态 | `money`, `gem`, `love_letter`, `warning`, `no_entry`, `busy`, `free`, `secret` |
| 创意/兴趣 | `goal`, `puzzle`, `music`, `headphones`, `sound`, `mute`, `eye`, `ear`, `nose`, `footprints` |
| 健康/医疗 | `bone`, `microbe`, `pill`, `syringe`, `thermometer` |
| 工业/科学符号 | `magnet`, `gear`, `atom`, `dna`, `biohazard`, `radioactive`, `bio` |
| 植物/自然 | `four_leaf`, `maple`, `cherry`, `tulip`, `rose`, `hibiscus`, `shell`, `feather` |
| 装饰/特殊 | `sparkle`, `diamond`, `fleur`, `comet` |

**非 emoji 绘制元素**（对应 Remotion elem_fns 特殊绘制逻辑）：

| key | Remotion 绘制方式 | emoji 映射 |
|-----|-------------|-----------|
| `brain` | 椭圆形光晕 | 🧠 |
| `neural_network` | 网格节点阵列 | 🧠 |
| `terminal` | 深色圆角矩形 | 💻 |
| `math_canvas` | 深色矩形 | 📐 |
| `ai_chip` | 方形芯片轮廓 | 🤖 |
| `spotlight` | 多层椭圆光晕 | 🔦 |
| `network_node` | 网格节点阵列 | 🔗 |
| `button` | 圆角矩形按钮 | 🔘 |
| `code` | 代码窗口+注释行 | 💻 |
| `algorithm` | 流程图方块+箭头 | 🔣 |
| `function` | ƒ(x)= 符号 | ƒ |
| `variable` | x = ??? 三连问号 | x |
| `bio` | DNA 双螺旋 | 🌱 |
| `secret` | \*\*\* + CLASSIFIED 印章 | \*\*\* |
| `lightning` | emoji 渲染 | ⚡ |
| `heart` | emoji 渲染 | ❤ |
| `equals_sign` | 等号文本 | ＝ |
| `question_mark` | 问号文本 | ？ |
| `eraser` | emoji 渲染 | 🧹 |
| `checkmark` | 对勾文本 | ✓ |

