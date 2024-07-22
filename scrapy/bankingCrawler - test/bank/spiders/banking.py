from __future__ import annotations
from scrapy.spiders import CrawlSpider, Rule

from typing import Generator
from urllib.parse import urljoin

from scrapy import Request 
from scrapy.responsetypes import Response
from scrapy.linkextractors import LinkExtractor

from bank.items import BankItem


class BankingSpider(CrawlSpider):
    name = "banking"
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/search?q=banking&c=apps"]

    rules = (
        Rule(LinkExtractor(allow='/store/apps/details'), callback="parse", follow=True, process_links="filter_links"),
    )

    custom_settings = {
        "FEEDS": {
            "output.json": {"format": "json"},
        },
    }

    def parse(self, response: Response) -> Generator[BankItem | Request, None, None]:
        """
        Parse the web page response.

        Args:
            response: The web page response.

        Yields:
            Yields scraped TitleItem and Requests for links.
        """
        self.logger.info('TitleSpider is parsing %s...', response)

        # Extract and yield the TitleItem
        url = response.url
        title = response.css('.DdYX5::text').extract_first()
        bank_name = response.css('.wMUdtb::text').get()
        rating = response.css('.w2kbF::text').get()

        yield BankItem(url=url, title=title, bank_name=bank_name, rating=rating)

        # Extract all links from the page, create Requests out of them, and yield them
        for link_href in response.css('a.Si6A0c.Gy4nib::attr("href")'):
            link_url = urljoin(response.url, link_href.get())
            if link_url.startswith(('http://', 'https://')):
                yield Request(link_url)