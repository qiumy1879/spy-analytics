import scrapy


class ListingItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()
    company_size = scrapy.Field()
    company_industry = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    published_at = scrapy.Field()

