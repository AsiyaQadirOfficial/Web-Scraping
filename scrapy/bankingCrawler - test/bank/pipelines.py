# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

"""
Scrapy item pipelines module

This module defines Scrapy item pipelines for scraped data. Item pipelines are processing components
that handle the scraped items, typically used for cleaning, validating, and persisting data.

For detailed information on creating and utilizing item pipelines, refer to the official documentation:
http://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Spider
from bank.items import BankItem


class BankPipeline:
    # def process_item(self, item, spider):
    #     return item
    """
    This item pipeline defines processing steps for TitleItem objects scraped by spiders.
    """

    def process_item(self, item: BankItem, spider: Spider) -> BankItem:
        # Do something with the item here, such as cleaning it or persisting it to a database
        return item

