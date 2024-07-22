import scrapy
from scrapy.spiders import CrawlSpider, Rule


class BankingSpiderSpider(scrapy.Spider):
    name = "banking_spider"
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/search?q=banking"]

    def parse(self, response):
        pass
