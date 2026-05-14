import scrapy


class ListingItem(scrapy.Item):
    """爬虫数据项：定义从网站抓取的数据结构
    
    这个类定义了我们要从招聘网站等平台抓取的所有字段
    """
    
    # 职位/列表标题
    title = scrapy.Field()
    
    # 公司名称
    company = scrapy.Field()
    
    # 原始薪资格式（如 "15-25K"）
    salary = scrapy.Field()
    
    # 薪资下限（解析后，数字格式）
    salary_min = scrapy.Field()
    
    # 薪资上限（解析后，数字格式）
    salary_max = scrapy.Field()
    
    # 城市
    city = scrapy.Field()
    
    # 区域/区县
    district = scrapy.Field()
    
    # 标签/技能要求（JSON字符串或逗号分隔）
    tags = scrapy.Field()
    
    # 职位描述
    description = scrapy.Field()
    
    # 公司规模
    company_size = scrapy.Field()
    
    # 公司行业
    company_industry = scrapy.Field()
    
    # 数据来源（如 "boss_zhipin", "liepin" 等）
    source = scrapy.Field()
    
    # 原始数据的 URL
    source_url = scrapy.Field()
    
    # 发布时间
    published_at = scrapy.Field()
