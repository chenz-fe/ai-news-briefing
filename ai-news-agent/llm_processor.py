from openai import OpenAI
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

def summarize_news(news_list):
    """把几十条新闻喂给大模型，让它提炼出最好的几条"""
    if not news_list:
        return "今日没有抓取到新资讯哦。"
        
    print("正在呼叫 AI 大脑进行总结提炼...")
    
    # 把新闻列表转成文本格式喂给大模型
    news_text_lines = []
    for i, news in enumerate(news_list):
        news_text_lines.append(f"{i+1}. [{news['source']}] {news['title']}\n链接: {news['link']}")
        
    news_context = "\n".join(news_text_lines)
    
    # 这里是 Prompt (提示词) 的核心！这就是 AI Engineer 的价值所在
    prompt = f"""
你是一个风格理性、偏极客的 AI 观察者，请阅读以下过去 24 小时的 AI 新闻列表：

{news_context}

请基于这些信息，输出一份面向「普通小白 + AI 关注者」的《今日 AI 简报》，要求如下（务必全部满足）：

【输出格式（必须严格遵守）】
- **第一行**：必须是「摘要：」开头，后跟 1～2 句话，概括今日简报的核心内容（例如：今日重点包括 OpenAI 融资、DeepSeek 芯片突破、多款 AI 代理工具发布等）。这一行会用于列表页和详情页的简短描述，不要写空话，要具体点出当天关键点。
- **第二行**：空行。
- **正文**：从「## 1. 本周值得关注的 AI 产品和工具」开始，**不要**再写「AI 简报：xx月xx日」或「今日 AI 简报（日期）」等重复标题，也不要写一级标题（#）。

【整体风格】
- 语言风格：理性、科技感、偏极客风，解释清晰、避免炫技。
- 不要刻意搞笑，不要「吃瓜」语气，也不要网络段子。
- 所有结论和判断，都要尽量基于新闻内容本身，保持谨慎和克制。

【结构与内容】
用 Markdown 二级标题（##）划分 3 个大章节；每个具体条目用**三级标题（###）**写名称，便于排版区分：

## 1. 本周值得关注的 AI 产品和工具
- 从新闻中筛选 3–5 个与「产品 / 工具」高度相关的内容。
- 每个条目格式：
  - **### 产品/工具名称**（若无明确产品名可用「公司/项目 + 简短描述」）
  - **使用人群是谁**：一句话说明面向谁。
  - **为何值得关注**：1～2 条理性判断。
  - **链接与信源**：用 [原文链接](URL)（来源：XXX 媒体），链接文字必须写「原文链接」三个字。

## 2. 大模型在不同场景下的头部玩家
- 归纳不同任务场景下被提及或表现突出的模型（通用问答、编程助手、多模态、文生图等）。
- 每个场景下列 2～4 个代表模型，用 **### 场景名** 或 加粗子标题 区分；简要说明 + 信源，链接格式 [原文链接](URL)（来源：XXX）。

## 3. 今日值得关注的 AI 大事件与重要言论
- 筛选 3～5 条最值得关注的事件或观点。
- 每条用 **### 事件/主题名** 开头，然后：发生了什么、为什么值得关注、[原文链接](URL)（来源：XXX）。

【写作细节】
- 排版清晰：## / ###、列表、加粗合理使用，方便扫读。
- 正文中禁止出现「AI 简报：02月27日 最值得关注的进展」「今日 AI 简报（2026年2月28日）」这类重复标题。
- 可以适当用比喻，但要贴近技术和产品场景；归纳时用「从这些新闻可以推断出」「这透露出一个趋势」等表述，避免绝对化断言。
"""

    if not LLM_API_KEY:
        print("⚠️ 警告: 还没有配置大模型的 API_KEY，返回原始文本...")
        return "由于未配置 API KEY，无法生成总结。\n\n原始新闻：\n" + news_context

    try:
        # 初始化 OpenAI 客户端 (极其清爽的标准写法，兼容 DeepSeek / 通义千问 等)
        client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是一个资深 AI 导师。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用大模型失败: {e}")
        print("提示: 若在 GitHub Actions 运行，请到仓库 Settings → Secrets → Actions 中配置 LLM_API_KEY（必填），以及可选 LLM_BASE_URL、LLM_MODEL")
        return "调用大模型失败，请检查 API 配置。"

if __name__ == "__main__":
    # 测试一下（构造假数据）
    dummy_news = [{"source": "测试", "title": "OpenAI 发布新模型 GPT-5", "link": "http://test.com"}]
    print(summarize_news(dummy_news))
