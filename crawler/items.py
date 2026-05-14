import scrapy


class PaperItem(scrapy.Item):
    """论文数据项：定义从 arXiv 抓取的数据结构

    v0.1 - 数据分析版本：不包含摘要
    """

    # arXiv 论文 ID，如 "2301.12345"
    paper_id = scrapy.Field()

    # 论文标题
    title = scrapy.Field()

    # 作者列表（JSON 字符串存储）
    authors = scrapy.Field()

    # 发表时间
    published_at = scrapy.Field()

    # arXiv 分类列表（JSON 字符串存储），如 ["cs.AI", "cs.LG"]
    categories = scrapy.Field()

    # 关键词/tags（JSON 字符串存储）
    keywords = scrapy.Field()

    # 数据来源，固定为 "arxiv"
    source = scrapy.Field()

    # arXiv 页面 URL
    source_url = scrapy.Field()

    # PDF 下载链接
    pdf_url = scrapy.Field()

    # arXiv 最后更新时间
    last_updated = scrapy.Field()

    # 作者备注（可选）
    comments = scrapy.Field()

    # 期刊引用（可选，如已发表在期刊上）
    journal_ref = scrapy.Field()
