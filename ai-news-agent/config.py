import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# --- 配置信息 ---

# 1. RSS 信息源配置（固定一批国内外相对权威的科技 / AI 媒体与社区）
RSS_FEEDS = {
    # 开发者社区 / 综合技术
    "Hacker News (AI)": "https://hnrss.org/newest?q=AI",

    # 国外科技与 AI 媒体
    "MIT Technology Review": "https://www.technologyreview.com/rss/",
    "TechCrunch (Artificial Intelligence)": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",

    # 国内科技 / AI 媒体
    "36氪": "https://36kr.com/feed",
    "机器之心": "https://www.jiqizhixin.com/articles",
}

# 2. LLM 大模型配置 (适配 DeepSeek / 通义千问 等国内大模型)
# 注意：GitHub Actions 未设置的 secret 会传成空字符串，需用 or 回退默认值
LLM_API_KEY = (os.getenv("LLM_API_KEY") or "").strip()
LLM_BASE_URL = (os.getenv("LLM_BASE_URL") or "https://api.deepseek.com").strip()
LLM_MODEL = (os.getenv("LLM_MODEL") or "deepseek-chat").strip()
