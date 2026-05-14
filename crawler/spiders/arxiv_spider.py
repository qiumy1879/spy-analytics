import scrapy
import yaml
import os
import json
from datetime import datetime, timedelta
from crawler.items import PaperItem


class ArxivSpider(scrapy.Spider):
    """arXiv 论文爬虫

    使用 arXiv API 抓取论文数据
    """

    name = "arxiv"
    allowed_domains = ["arxiv.org", "export.arxiv.org"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = self._load_config()

    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config.yaml"
        )
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def start_requests(self):
        """生成起始请求"""
        config = self.config.get('arXiv', {})
        categories = config.get('categories', [])
        days_back = config.get('days_back', 7)
        max_results = config.get('max_results_per_request', 500)

        # 计算开始时间
        start_date = datetime.utcnow() - timedelta(days=days_back)
        start_date_str = start_date.strftime('%Y%m%d%H%M%S')

        # 为每个分类生成请求
        for category in categories:
            api_url = self._build_api_url(category, start_date_str, max_results)
            yield scrapy.Request(
                url=api_url,
                callback=self.parse,
                meta={'category': category}
            )

    def _build_api_url(self, category, start_date_str, max_results):
        """构建 arXiv API 请求 URL"""
        base_url = self.config.get('arXiv', {}).get(
            'api_base_url',
            'http://export.arxiv.org/api/query'
        )
        query = f"cat:{category} AND submittedDate:[{start_date_str} TO *]"
        return f"{base_url}?search_query={query}&start=0&max_results={max_results}"

    def parse(self, response):
        """解析 arXiv API 响应（待实现）

        注意：这是一个占位实现，实际需要根据 arXiv API
        返回的 XML 格式来解析
        """
        self.logger.info(f"Got response from {response.url}")
        self.logger.info("TODO: Implement XML parsing for arXiv API response")

        # TODO: 实际解析逻辑
        # 1. 解析 XML
        # 2. 提取论文数据
        # 3. 构建 PaperItem
        # 4. yield Item
