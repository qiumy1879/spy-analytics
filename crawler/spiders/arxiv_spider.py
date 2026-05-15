import scrapy
import yaml
import os
import json
from datetime import datetime, timedelta
import arxiv
from crawler.items import PaperItem


class ArxivSpider(scrapy.Spider):
    """arXiv 论文爬虫

    使用 arxiv.py 库抓取论文数据
    支持命令行参数自定义爬取范围
    
    使用示例：
    python -m scrapy crawl arxiv -a days=3 -a categories=cs.AI,cs.LG
    """

    name = "arxiv"
    allowed_domains = ["arxiv.org"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = self._load_config()
        
        # 从命令行参数覆盖配置（如果提供）
        self.days_back = int(getattr(self, 'days', self.config.get('arXiv', {}).get('days_back', 1)))
        
        # 解析分类参数（支持逗号分隔的多个分类）
        categories_arg = getattr(self, 'categories', None)
        if categories_arg:
            self.categories = [cat.strip() for cat in categories_arg.split(',')]
        else:
            self.categories = self.config.get('arXiv', {}).get('categories', [])
        
        self.max_results = self.config.get('arXiv', {}).get('max_results_per_request', 10)

    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config.yaml"
        )
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def start_requests(self):
        """生成起始请求 - 使用 arxiv.py 直接抓取"""
        self.logger.info(f"="*60)
        self.logger.info(f"开始爬取 arXiv 论文")
        self.logger.info(f"爬取天数：最近 {self.days_back} 天")
        self.logger.info(f"爬取分类：{', '.join(self.categories)}")
        self.logger.info(f"每类最多：{self.max_results} 篇")
        self.logger.info(f"="*60)
        
        # 计算开始时间
        start_date = datetime.utcnow() - timedelta(days=self.days_back)

        # 为每个分类抓取论文
        for category in self.categories:
            self.logger.info(f"正在处理分类：{category}")
            
            # 构建搜索查询
            query = f"cat:{category}"
            
            # 使用 arxiv.py 搜索
            search = arxiv.Search(
                query=query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )

            # 处理结果
            count = 0
            for result in search.results():
                # 检查论文是否在时间范围内
                if result.published.replace(tzinfo=None) < start_date:
                    continue
                
                # 构建 PaperItem
                item = PaperItem()
                item['paper_id'] = result.entry_id.split('/')[-1]
                item['title'] = result.title
                item['authors'] = json.dumps([author.name for author in result.authors])
                item['published_at'] = result.published.replace(tzinfo=None)
                item['categories'] = json.dumps(result.categories)
                item['keywords'] = json.dumps([])  # arXiv 没有直接的 keywords 字段
                item['source'] = 'arxiv'
                item['source_url'] = result.entry_id
                item['pdf_url'] = result.pdf_url
                item['last_updated'] = result.updated.replace(tzinfo=None) if result.updated else None
                item['comments'] = result.comment
                item['journal_ref'] = result.journal_ref
                
                count += 1
                self.logger.info(f"  [{count}] 抓取论文：{item['paper_id']} - {item['title'][:50]}...")
                
                yield item
            
            self.logger.info(f"分类 {category} 完成，共抓取 {count} 篇论文")

    def parse(self, response):
        """这个方法不会被调用，因为我们直接在 start_requests 中处理了"""
        pass
