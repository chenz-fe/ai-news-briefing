import feedparser
from datetime import datetime, timedelta
import time
from config import RSS_FEEDS

def fetch_daily_news():
    """抓取过去 24 小时的 AI 新闻"""
    print("开始抓取今日 AI 新闻...")
    all_news = []
    
    # 计算24小时前的时间戳
    yesterday = time.time() - 24 * 60 * 60

    for source_name, feed_url in RSS_FEEDS.items():
        print(f"正在读取信源: {source_name}")
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                # 解析发布时间
                # 如果没有 published_parsed，尝试用 updated_parsed
                published_time = entry.get('published_parsed', entry.get('updated_parsed'))
                if published_time:
                    entry_timestamp = time.mktime(published_time)
                    if entry_timestamp > yesterday:
                        all_news.append({
                            "source": source_name,
                            "title": entry.title,
                            "link": entry.link,
                            # summary 有时候带有很多 HTML 标签，可以暂存
                            "summary": entry.get('summary', '')[:200] + "..." 
                        })
        except Exception as e:
            print(f"读取 {source_name} 失败: {e}")
            
    print(f"抓取完成！共获取 {len(all_news)} 条近期新闻。")
    return all_news

if __name__ == "__main__":
    # 测试一下爬虫模块
    news = fetch_daily_news()
    for n in news[:3]:
        print(f"[{n['source']}] {n['title']}")
