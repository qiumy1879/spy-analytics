# Scrapy 设置
BOT_NAME = "spy_analytics_crawler"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

# 遵守 robots.txt（arXiv 的 robots.txt 允许爬取）
ROBOTSTXT_OBEY = True

# 下载延迟，防止请求太快
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# 默认请求头
DEFAULT_REQUEST_HEADERS = {
    "Accept": "application/atom+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent": "SpyAnalytics/0.1 (+https://github.com/qiumy1879/spy-analytics)",
}

# 项目管道
ITEM_PIPELINES = {
    "crawler.pipelines.PaperPipeline": 300,
}

# 日志级别
LOG_LEVEL = "INFO"
