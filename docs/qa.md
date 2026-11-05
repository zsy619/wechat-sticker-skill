## 质量保障与运维

## 质量检查清单

### 自动化检查（qa_check.py）

推荐优先使用自动化检查脚本：

```bash
python3 scripts/qa_check.py \
  --input assets-cyberpunk/ \
  --vocabulary docs/prompts-format.md \
  --prompts prompts/
```

**检查项目（可自动化的）**：

| 检查项 | 类型 | 说明 |
|--------|------|------|
| 文件尺寸 | 自动 | 所有贴图必须 1080×1440px |
| 文件格式 | 自动 | 必须为 PNG 或 GIF |
| 双格式齐全 | 自动/人工 | 每个序号须同时有 `.gif` 与 `.png`（交付不得缺一） |
| 文件名格式 | 自动 | 必须符合 `{num}-{name}.png` 或 `.gif` |
| 词汇表校验 | 自动 | visual_elements 中的 key 必须在词汇表范围内 |
| 文件完整性 | 自动 | 所有 prompts 对应的输出文件必须存在 |

### 手动复核（其余项目）

生成完成后，按以下清单逐项检查：

- [ ] 贴图风格保持一致（同一--theme）
- [ ] 文字清晰可读，底部居中、左右边距30px、距底边30px
- [ ] 每张贴图copy字段≥10字
- [ ] 底部文字清晰可读（无截断、无遮挡）
- [ ] 主题色应用正确
- [ ] 每张贴图数量 ≥ 6 张（标准配置）
- [ ] 标签推荐已生成（5-10个）
- [ ] 内容聚合分析完整准确
- [ ] 标签推荐覆盖全面（每张≥5个标签）
- [ ] 同一项目多风格生成（如需）：分别存放于 `assets-{theme}/` 目录
- [ ] session-log.md 统计文件已生成（模板见 references/token-stats.md）

---

## 故障排除

### 网络搜索失败

- **解决方案**：跳过搜索步骤，直接使用原始输入
- **影响**：内容分析可能不够全面，但不影响生成

### Remotion 导出失败

- **症状**：`npx remotion still` 报错
- **原因**：Node.js 不可用 / 组件编译错误 / 版本不兼容
- **解决方案**：检查 Node.js 安装，升级 Remotion 版本

### 目录冲突

- **解决方案**：添加时间戳后缀
- **格式**：`{slug}-YYYYMMDD-HHMMSS/`

### 图片尺寸问题

- **微信贴图标准**：1080×1440px
- **文件格式**：同时保留 PNG 与 GIF（同序号同名；PNG 可透明或主题背景）
- **如需调整**：使用 ffmpeg `scale` 和 `crop` 滤镜

### 字体缺失

- **症状**：Remotion 渲染时文字为默认字体或警告
- **原因**：系统字体路径不存在
- **解决方案**：安装中文字体（macOS: `brew install font-cctia` 或从 App Store 安装）

## Remotion 已知问题

### Sequence + AbsoluteFill 居中失效

- **症状**：Remotion 导出的帧中文字为空白/透明（max channel ~100 而非 255），无控制台报错
- **根因**：在 `Sequence` 内直接放 `AbsoluteFill` 并用 `justifyContent: 'center'` 居中，Chrome headless 下 centering 完全失效
- **解决**：场景拆为独立组件，`AbsoluteFill` 放在 Scene 组件内部，不直接放在 `Sequence` 下

### Chrome headless SSL 错误

- **症状**：`unable to get local issuer certificate` 导致 Remotion 无法下载 Chrome
- **解决**：在 `remotion.config.ts` 中指定系统 Chrome（macOS）：

```ts
import { Config } from '@remotion/cli/config';
Config.setBrowserExecutable('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
```

### 渲染崩溃（frame 2500-3000）

- **症状**：复杂动画在长帧数时 Chrome headless 崩溃
- **解决**：
  - 减少每帧动画元素数量
  - 用 CSS 渐变替代动画 SVG
  - 超过 60 秒的视频分段渲染（~30s/段）

### `registerRoot` 直接传组件导致 hooks 失效

- **症状**：`useCurrentFrame() can only be called inside a component that is part of a composition`
- **根因**：`registerRoot(MyVideo)` 绕过了 Remotion Composition 上下文
- **解决**：使用 Root 组件 + `<Composition id="X" component={MyVideo} .../>` 包装

### 包版本冲突

- **症状**：`delayRender() timeout`、`React context lost`
- **根因**：多个 Remotion 版本同时存在于 `node_modules`
- **解决**：`package.json` 固定 `"remotion": "4.0.448"`，只安装 `remotion` 包（不装 `@remotion/core` 等不存在的 v4 包）

### Remotion CLI 调试技巧

#### `remotion still` 报错 `width prop must be a number`

- **症状**：`npx remotion still src/index.tsx StickerComponent` 报错 `width prop must be a number, but passed undefined`
- **根因**：Discovery 阶段 Remotion 调用 `StickerComponent(undefined)`，`<Composition>` 的 `width={width}` 没有默认值
- **解决**：在 `<Composition>` 属性中使用 `??` 提供 fallback：

```tsx
<Composition
  durationInFrames={totalFrames ?? 720}
  fps={fps ?? 30}
  width={width ?? 1080}
  height={height ?? 1440}
/>
```

#### 验证修复

修复后执行：

```bash
cd ~/wechat-stickers/{项目名}/remotion-sticker/
npx remotion still src/index.tsx StickerComponent --output /tmp/test-still.png
```

成功输出示例：

```
Your still frame is ready! Output: out/StickerComponent.png
Rendering time: 4s
```

注意：输出尺寸可能略大于预期的 `width×height`（如 1523×2030 而非 1080×1440），这是 Remotion 内部缩放行为，不影响内容正确性。

#### 确认 ?? fallback 不干扰正常渲染

正式渲染时，`??` fallback 只在 Discovery 阶段（props=undefined）生效；正常渲染时 `<Composition>` 仍从外层 props 取值。验证方式：

```bash
npx remotion render src/index.tsx StickerComponent \
  --props '{"totalFrames":540,"fps":30,"width":1080,"height":1440}' \
  --output out/
```

若输出视频帧尺寸为 1080×1440（而非 fallback 的 1523×2030），说明正常渲染取值正确。
