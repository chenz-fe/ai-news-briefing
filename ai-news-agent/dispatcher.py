def _parse_summary_and_content(raw_markdown):
    """从 LLM 原始输出中解析第一行「摘要：xxx」，返回 (description, content)。
    若没有摘要行，description 为 None，content 为全文。
    """
    if not raw_markdown or not isinstance(raw_markdown, str):
        return None, raw_markdown or ""
    stripped = raw_markdown.strip()
    if stripped.startswith("摘要："):
        first_line_end = stripped.find("\n")
        if first_line_end == -1:
            summary_line = stripped
            rest = ""
        else:
            summary_line = stripped[:first_line_end]
            rest = stripped[first_line_end:].lstrip("\n")
        description = summary_line.replace("摘要：", "", 1).strip()
        return description or None, rest
    return None, stripped


def save_to_markdown(title, raw_content_markdown, output_dir="daily_reports"):
    """把生成的简报保存到独立文件夹，并添加标准博客/SSG 所需的 YAML Frontmatter。

    - 若 raw_content_markdown 第一行以「摘要：」开头，会解析为 description 写入 frontmatter，并从正文中去掉该行。
    - Frontmatter 字段：title, date, description, slug（供 Next.js + gray-matter 使用）。
    """
    import os
    from datetime import datetime

    description, content_markdown = _parse_summary_and_content(raw_content_markdown)
    if description is None:
        description = "今日 AI 领域的最新产品、模型进展与大事件简报。"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_str}_AINews.md"
    filepath = os.path.join(output_dir, filename)

    title_escaped = (title or "").replace('\\', '\\\\').replace('"', '\\"')
    desc_escaped = (description or "").replace('\\', '\\\\').replace('"', '\\"')

    frontmatter = f"""---
title: "{title_escaped}"
date: {today_str}
description: "{desc_escaped}"
slug: "{today_str}"
---

"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter)
        f.write(content_markdown)

    print(f"✅ 简报已保存到本地: {filepath}")
    return filepath
