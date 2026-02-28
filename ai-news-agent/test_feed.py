import feedparser
import time
feed = feedparser.parse("https://www.jiqizhixin.com/rss")
print("Total entries:", len(feed.entries))
if feed.entries:
    e = feed.entries[0]
    print("Keys in entry:", e.keys())
    print("published_parsed:", e.get('published_parsed'))
    print("updated_parsed:", e.get('updated_parsed'))
    print("published:", e.get('published'))
