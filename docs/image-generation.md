# 图片生成（两段式工作流）

## 优先级总览

```
┌─────────────────────────────────────────┐
│  阶段一：AI 生成图像（首选）             │
│  调用大模型直接生成高质量帧              │
│  失败 → 降级到 Remotion                 │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│  阶段二：Remotion 帧导出（第二选择）     │
│  每张贴图 = <Composition> → render 导出 GIF│
│  失败 → 报错停止（不再降级）           │
└─────────────────────────────────────────┘
```

## 阶段一 · AI 生成（首选）

**适用**：所有贴图，追求最高视觉质量。产出 **PNG 静图**；下游须再导出同名 GIF，PNG 成品保留。

### 支持的 Provider

| 优先级 | Provider | 模型 | 备注 |
|--------|----------|------|------|
| 1 | `dashscope` | qwen-image-2.0-pro | 账户欠费时跳过 |
| 2 | `seedream` | doubao-seedream-5-0-260128 | 账户欠费时跳过 |
| 3 | `minimax` | image-01 | 未配置时跳过 |
| 4 | `openai` | gpt-image-1.5 | 未配置时跳过 |

### 提示词构建

```bash
python3 -c "
import json, glob, yaml

items = []
for pf in glob.glob('prompts/*.md'):
    with open(pf) as f:
        front = {}
        for l in f:
            if l.strip() == '---': break
            if ':' in l:
                k, v = l.split(':', 1)
                front[k.strip()] = v.strip().strip('\"').strip(\"'\")
    name = front.get('name', '')
    copy = front.get('copy', '')
    style = front.get('style_keyword', '')
    theme = front.get('theme', 'cyberpunk')
    prompt = f'微信贴图，1080x1440px，3:4竖版，文字: {copy}，风格: {style}，高质量，精致细节'
    items.append({'name': name, 'prompt': prompt})

with open('batch.json', 'w') as f:
    json.dump({'items': items}, f, ensure_ascii=False, indent=2)
"
```

### 异常处理

- **401/欠费** → 跳过该 provider，尝试下一个
- **429限流** → 等待10秒重试（最多3次）
- **超时（>60s）** → 降级到 Remotion
- **所有 provider 失败** → 降级到 Remotion

## 阶段二 · Remotion 帧导出（第二选择）

**适用**：需要精确控制视觉元素、程序化绘制，或 AI 生成失败后的备选。默认导出 GIF；另保留/导出同名 PNG Still。

### 流程

```
prompts/*.md
    ↓（每张贴图）
生成 {StickerName}.tsx 组件
    ↓
创建 remotion/{sticker-name}/ 项目
    ↓
npx remotion render → GIF
    ↓
输出到 assets/
```

详见 [frame-design.md](frame-design.md)。

### 项目初始化

```bash
mkdir -p remotion/{sticker-name}/src
```

### 导出 GIF（带动画）

> 注意：本项目使用 Remotion **渲染 GIF 动画**（每贴图 90 帧 @30fps），而非导出单帧 PNG Still。
> `npx remotion still` 用于导出单帧 PNG；`npx remotion render` 用于导出多帧 GIF/MP4。

```bash
cd remotion/{sticker-name}
npx remotion render src/index.tsx StickerComponent \
  --output ../../assets/{sticker-name}.gif \
  --frames 0-89 --fps 30
```

### 异常处理

- **Node.js 不可用** → 报错停止
- **npx remotion 报错** → 报错停止
- **组件编译错误** → 记录错误，跳过该贴图

## 贴图生成核心规则（所有阶段适用）

- **尺寸**：1080×1440px（微信贴图标准）
- **格式**：同时保留 **GIF + PNG**（同序号同名）；不得只留一种
- **文字**：底部居中，左右 margin 30px，距底边 30px
- **文件名**：`{num}-{name}.png` 与 `{num}-{name}.gif`
- **分发**：GIF → 公众号/贴图推送；PNG → 抖音/小红书（标题 ≤20 字）

### AI 路径与双格式

1. AI 先出 **PNG**（静图 / 中间帧）→ **必须保留**（抖音/小红书用）。
2. 同序号再导出 **GIF**（Remotion 动画，或由帧序列合成）→ 公众号/贴图推送默认用 GIF。
3. 禁止「转成 GIF 后删 PNG」或「只交 PNG 不交 GIF」。

## 输出格式

无论哪个阶段生成，最终 `assets-{theme}/` 须同时有：

```
assets-{theme}/
├── 01-{name}.gif   ← 1080×1440px GIF（公众号/贴图推送）
├── 01-{name}.png   ← 同序号 PNG（抖音/小红书；AI 静图或 Remotion Still）
├── 02-{name}.gif
├── 02-{name}.png
└── ...
```
