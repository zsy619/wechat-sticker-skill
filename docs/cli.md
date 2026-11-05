# 命令行参考（分步执行与参数）

> 何时读：需要分步调试、补跑某一步、或查 `generate_frames.py` / `pack_stickers.py` 参数时。完整流程只需 SKILL.md 里的一条命令。
> 所有脚本均支持 `--help`，以 `--help` 输出为准，不读源码。

## 分步执行（调试用）

```bash
# 步骤1：内容聚合分析
python3 scripts/generate_content_analysis.py \
  --input "AI编程助手" \
  --output ~/wechat-stickers/ai-coding-assistant/

# 步骤2：生成 manifest
python3 scripts/generate_manifest.py \
  --input ~/wechat-stickers/ai-coding-assistant/content-analysis.md \
  --output ~/wechat-stickers/ai-coding-assistant/sticker-manifest.md

# 步骤3：生成 prompts
python3 scripts/generate_prompts.py \
  --input ~/wechat-stickers/ai-coding-assistant/sticker-manifest.md \
  --output ~/wechat-stickers/ai-coding-assistant/prompts/

# 步骤4：图片生成（两段式：AI → Remotion）
python3 scripts/generate_frames.py \
  --input ~/wechat-stickers/ai-coding-assistant/prompts/ \
  --output ~/wechat-stickers/ai-coding-assistant/assets-cyberpunk/ \
  --theme cyberpunk

# 步骤5：打包 + QA 检查
python3 scripts/pack_stickers.py \
  --input ~/wechat-stickers/ai-coding-assistant/assets-cyberpunk/ \
  --output ~/wechat-stickers/ai-coding-assistant/stickers.zip

python3 scripts/qa_check.py \
  --input ~/wechat-stickers/ai-coding-assistant/assets-cyberpunk/ \
  --vocabulary docs/prompts-format.md
```

### --mode 参数

`generate_frames.py` 支持强制指定生成模式：

| 值 | 行为 |
|----|------|
| `auto`（默认） | AI → Remotion 两段式 |
| `ai` | 仅 AI 生成，失败则整张贴图失败 |
| `remotion` | 仅 Remotion 生成，失败则报错 |

### 新增参数（v4.4.0）

| 参数 | 说明 |
|------|------|
| `--continue-on-error` | 某张贴图失败时跳过继续处理下一张 |
| `--debug-remotion` | 保留 Remotion 调试文件（TSX 源码写入 `debug/` 目录） |
| `--template-dir` | 自定义 Remotion 模板目录（覆盖内置模板 `remotion/template/`） |
| `--remotion-version` | 指定 Remotion 版本（default: `4.0.448`） |
| `--dry-run` | 仅解析 `.md` 文件并打印生成计划，不生成任何文件 |

`pack_stickers.py` 参数：

| 参数 | 说明 |
|------|------|
| `--gif-only` | 只打包 GIF 文件，忽略 PNG/JPG |
| `--png-only` | 只打包 PNG 文件，忽略 GIF/JPG |

## 补跑缺失文档

**补跑命令**：pipeline 中断后，可使用以下命令单独生成缺失文档：
```bash
python3 scripts/generate_tags.py --input sticker-manifest.md --output tags.md --theme cyberpunk
python3 scripts/generate_session_log.py --project <name> --theme cyberpunk --sticker-count 8 --output session-log.md
python3 scripts/generate_post.py --project ~/wechat-stickers/<project> --theme cyberpunk --output post.md
```
