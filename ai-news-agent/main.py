from fetcher import fetch_daily_news
from llm_processor import summarize_news
from dispatcher import save_to_markdown
from datetime import datetime

def run_agent():
    print("🚀 启动 AI News Agent 工作流...")
    
    # 第一步：抓取数据
    raw_news = fetch_daily_news()
    
    if not raw_news:
        print("今天没有抓到任何新闻，流程结束。")
        return
        
    # 第二步：大模型提炼总结
    summary_markdown = summarize_news(raw_news)
    
    # 第三步：保存到本地
    today_str = datetime.now().strftime("%m月%d日")
    report_title = f"AI 简报：{today_str} 最值得关注的进展"
    
    save_to_markdown(report_title, summary_markdown)
    
    print("🎉 AI News Agent 工作流执行完毕！（已保存为本地 Markdown 文件）")

if __name__ == "__main__":
    run_agent()
