#!/usr/bin/env python3
"""
generate_post.py - 生成多平台贴图推广草稿（默认公众号）

基于 manifest 生成草稿文案；只进草稿箱，不直接发布。
无特别说明时定时窗口 19:00–22:00（Asia/Shanghai）；用户说「立即发」才立即发。

平台：
  wechat（默认）→ GIF 素材配文，输出 post.md
  douyin / xhs  → PNG 素材配文，标题严格 ≤20 字，输出 post-douyin.md / post-xhs.md

Usage:
    python3 scripts/generate_post.py \
        --project ~/wechat-stickers/opengeometry \
        --theme neon \
        --platform wechat \
        --output post.md
"""

import os
import re
import random
import argparse
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

# ── 标题模板库 ────────────────────────────────────────────

# 公众号（GIF）标题模板；填充后仍截断至 ≤20 字
TITLE_TEMPLATES = [
    "「{project}」微信表情包上新",
    "{project} 专属表情包来了",
    "{project} 趣味表情包上新",
    "{project} 定制贴图上新",
    "【{project}】贴图草稿待发",
    "{project} 主题表情包上新",
]

# 抖音 / 小红书（PNG）短标题；务必 ≤20 字
TITLE_TEMPLATES_SHORT = [
    "{project} 表情包上新",
    "这套 {project} 贴图好看",
    "{project} 静图贴图来了",
    "存下 {project} 表情包",
]

PLATFORM_DEFAULT_OUTPUT = {
    "wechat": "post.md",
    "douyin": "post-douyin.md",
    "xhs": "post-xhs.md",
}


# ── 平台标签（固定） ─────────────────────────────────────

PLATFORM_TAGS = ["微信表情", "微信贴图", "WeChatStickers"]


# ── 信息提取 ─────────────────────────────────────────────


def extract_info(project_root, theme, link):
    """从项目目录提取信息用于生成 post"""

    manifest_path = os.path.join(project_root, "sticker-manifest.md")
    tags_path = os.path.join(project_root, "tags.md")
    content_path = os.path.join(project_root, "content-analysis.md")
    prompts_dir = os.path.join(project_root, "prompts")

    # 优先从 prompts frontmatter 的 name 字段获取项目名（最可靠）
    # 降级：manifest 第一行 / content-analysis 第一行 / 目录名
    project_name = None

    if os.path.isdir(prompts_dir):
        for fname in sorted(os.listdir(prompts_dir)):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(prompts_dir, fname)
            with open(fpath) as f:
                raw = f.read()
            # 取第一个文件的 frontmatter name
            front = {}
            in_front = False
            for line in raw.split('\n'):
                if line.strip() == '---':
                    if not in_front:
                        in_front = True
                    else:
                        break
                if in_front and ':' in line:
                    k, v = line.split(':', 1)
                    front[k.strip()] = v.strip().strip('"').strip("'")
            if 'name' in front:
                project_name = front['name']
                break

    # 降级取目录名（避免取到技能根目录名）
    if not project_name:
        project_name = os.path.basename(os.path.abspath(project_root.rstrip('/')))

    # 优先从 manifest 的项目信息节提取真实项目名（覆盖上述 fallback）
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            m_content = f.read()
        # 匹配 "**项目名称**: value" 或 "- **项目名称**: value"
        m = re.search(r'\*{0,2}项目名称\*{0,2}:\s*(.+)', m_content)
        if m:
            project_name = m.group(1).strip()

    stickers_count = 0
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            content = f.read()
        patterns = [
            r"^## sticker_\d+",
            r"^## (?:\d+[.-]|贴图\d+:)",
        ]
        for pat in patterns:
            matches = re.findall(pat, content, re.MULTILINE)
            if matches:
                stickers_count = len(matches)
                break

    tags = []
    if os.path.exists(tags_path):
        with open(tags_path) as f:
            content = f.read()
        found_tags = re.findall(r"\*\*([^*]+)\*\*", content)
        tags = [t.strip() for t in found_tags if len(t.strip()) >= 2][:10]

    description = ""
    if os.path.exists(content_path):
        with open(content_path) as f:
            content = f.read()
        sections = content.split("---")
        for section in sections:
            if "核心功能" in section or "项目概述" in section or "## 项目" in section:
                lines = []
                for line in section.split("\n"):
                    stripped = line.strip()
                    if (
                        stripped.startswith("#")
                        or not stripped
                        or stripped.startswith("|")
                        or stripped.startswith("- **")
                        or stripped.startswith("**")
                    ):
                        continue
                    if len(stripped) > 20:
                        lines.append(stripped)
                if lines:
                    description = " ".join(lines[:2])
                    break

    all_tags = PLATFORM_TAGS + tags
    seen = set()
    unique_tags = []
    for t in all_tags:
        if t not in seen:
            seen.add(t)
            unique_tags.append(t)

    return {
        "project": project_name,
        "theme": theme,
        "link": link,
        "count": stickers_count,
        "tags": unique_tags,
        "description": description,
    }


def extract_manifest_details(project_root):
    """提取 manifest 中的贴图详情"""
    manifest_path = os.path.join(project_root, "sticker-manifest.md")
    manifest_content = ""
    sticker_details = []
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            manifest_content = f.read()
        sections = re.split(r"^## 贴图\d+:", manifest_content, flags=re.MULTILINE)
        for s in sections[1:]:
            name_match = re.search(r"\*\*名称\*\*:\s*(.+)", s)
            copy_match = re.search(r"\*\*核心文案\*\*:\s*(.+)", s)
            if name_match:
                sticker_details.append(
                    {
                        "name": name_match.group(1).strip(),
                        "copy": copy_match.group(1).strip() if copy_match else "",
                    }
                )
    return sticker_details


def extract_project_desc(project_root):
    """提取 content-analysis 中的项目描述"""
    content_path = os.path.join(project_root, "content-analysis.md")
    if os.path.exists(content_path):
        with open(content_path) as f:
            c = f.read()
        match = re.search(r"## 核心主题\s*\n+(.*?)(?=\n##|\Z)", c, re.DOTALL)
        if match:
            return match.group(1).strip()[:300]
    return ""


# ── 主函数


def generate_title(project, theme, platform="wechat"):
    pool = TITLE_TEMPLATES_SHORT if platform in ("douyin", "xhs") else TITLE_TEMPLATES
    # 短项目名优先大写，避免标题被截到半个词
    proj = project.upper() if len(project) <= 8 else project
    # 预留模板填充后 ≤20：过长项目名先截
    max_proj = 12 if platform in ("douyin", "xhs") else 14
    if len(proj) > max_proj:
        proj = proj[:max_proj]
    template = random.choice(pool)
    title = template.format(project=proj)
    title = title[:20].rstrip("，、。；：")
    return title


def generate_content(info):
    project = info["project"]
    theme = info["theme"]
    link = info["link"]
    count = info["count"]
    description = info["description"]

    theme_names = {
        "neon": "霓虹科技",
        "cyberpunk": "赛博朋克",
        "kawaii": "可爱治愈",
        "retro": "复古怀旧",
        "hand-drawn": "手绘文艺",
        "minimal": "简约冷淡",
        "meme": "搞笑网络",
    }
    theme_cn = theme_names.get(theme, theme)

    content_parts = []

    if description:
        content_parts.append(
            f"给大家介绍一套专为 {project} 量身定制的微信表情包！"
            f"这套表情以 {theme_cn} 风格呈现，收录了 {count} 张精心设计的动态贴图，"
            f"每一张都捕捉了开发者日常工作中的精彩瞬间。"
        )
    else:
        content_parts.append(
            f"一套专为 {project} 开发者打造的微信表情包来啦！"
            f"以 {theme_cn} 风格呈现，包含 {count} 张精心设计的动态贴图，"
            f"让你的聊天更加生动有趣。"
        )

    if link:
        content_parts.append(
            f"无论是调试代码时的兴奋、解决 Bug 后的成就感，还是迎接新项目时的期待——"
            f"这套表情包都能准确表达工程师的心声。"
            f"现在就去体验吧：{link}"
        )
    else:
        content_parts.append(
            f"无论是调试代码时的兴奋、解决 Bug 后的成就感，还是迎接新项目时的期待——"
            f"这套表情包都能准确表达工程师的心声。"
        )

    content_parts.append(
        f"喜欢这套 {project} 主题表情包吗？快去微信表情包商店搜索「{project}」下载使用吧！"
    )

    return "\n\n".join(content_parts)


def generate_tags_line(tags):
    selected = tags[:8]
    if len(selected) < 5:
        defaults = ["AI", "人工智能", "程序员", "代码", "科技"]
        for d in defaults:
            if d not in selected:
                selected.append(d)
            if len(selected) >= 5:
                break
    return "#" + " #".join(selected[:8])


def generate_post(project_root, theme, link, output, title=None, verbose=True, platform="wechat"):
    """生成多平台推广草稿（结构化模板）；只进草稿箱。"""

    platform = (platform or "wechat").lower()
    if platform not in PLATFORM_DEFAULT_OUTPUT:
        raise ValueError(f"unsupported platform: {platform}")

    info = extract_info(project_root, theme, link)

    if not title:
        title = generate_title(info["project"], theme, platform=platform)
    if title:
        title = title[:20].rstrip("，、。；：")

    content = generate_content(info)
    tags_line = generate_tags_line(info["tags"])
    asset = "gif" if platform == "wechat" else "png"

    doc = f"""---
name: {info['project']}-post
title: {title}
theme: {theme}
platform: {platform}
asset: {asset}
status: draft
schedule_window: 19:00-22:00 Asia/Shanghai
date: {date.today().isoformat()}
tags: {tags_line}
link: {link or ''}
---

> 草稿箱文案。无「立即发」则定时 19:00–22:00（Asia/Shanghai）。
> 配图：{'公众号/贴图推送用同序号 GIF' if platform == 'wechat' else '抖音/小红书用同序号 PNG（标题已 ≤20 字）'}。

{content}

## 标签

{tags_line}
"""

    os.makedirs(os.path.dirname(os.path.abspath(output)) or ".", exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        f.write(doc)

    if verbose:
        print(f"✅ 推广草稿已生成（{platform}/{asset}）: {output}")
        print(f"   标题: {title}（{len(title)}字，上限20）")
        print(f"   贴图: {info['count']} 张｜状态: 草稿箱｜窗口: 19:00-22:00 Asia/Shanghai")
        print(f"   标签: {tags_line}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="生成多平台贴图推广草稿（默认公众号；只进草稿箱）")
    parser.add_argument("--project", required=True, help="项目目录")
    parser.add_argument("--theme", required=True, help="主题")
    parser.add_argument("--link", default="", help="项目链接")
    parser.add_argument("--platform", default="wechat",
                       choices=["wechat", "douyin", "xhs"],
                       help="wechat=GIF 配文；douyin/xhs=PNG 配文，标题≤20")
    parser.add_argument("--output", default=None,
                       help="输出路径（默认 post.md / post-douyin.md / post-xhs.md）")
    parser.add_argument("--title", default=None, help="自定义标题（不超过20字符）")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--verify", action="store_true",
                       help="仅验证输入文件，不生成文档")
    args = parser.parse_args()

    # --verify 模式：检查依赖文件是否存在
    if args.verify:
        project_root = os.path.abspath(args.project)
        manifest = os.path.join(project_root, "sticker-manifest.md")
        tags = os.path.join(project_root, "tags.md")
        prompts = os.path.join(project_root, "prompts")
        content = os.path.join(project_root, "content-analysis.md")
        print("[verify] 检查项目依赖文件...")
        all_ok = True
        for path, label in [(manifest, "manifest"), (tags, "tags"), (prompts, "prompts/"), (content, "content-analysis")]:
            exists = os.path.exists(path)
            status = "✅" if exists else "❌"
            print(f"  {status} {label}: {path}")
            if not exists:
                all_ok = False
        print(f"\n{'✅ 所有依赖文件就绪' if all_ok else '❌ 缺少依赖文件'}")
        return 0 if all_ok else 1

    output = args.output or PLATFORM_DEFAULT_OUTPUT[args.platform]
    # 相对路径落到项目根，避免写到调用 cwd
    if not os.path.isabs(output):
        output = os.path.join(os.path.abspath(args.project), output)

    return (
        0
        if generate_post(
            project_root=os.path.abspath(args.project),
            theme=args.theme,
            link=args.link,
            output=output,
            title=args.title,
            verbose=not args.quiet,
            platform=args.platform,
        )
        else 1
    )


if __name__ == "__main__":
    sys.exit(main())
