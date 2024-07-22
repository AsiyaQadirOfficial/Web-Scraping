# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


"""
Scrapy item models module

This module defines Scrapy item models for scraped data. Items represent structured data
extracted by spiders.

For detailed information on creating and utilizing items, refer to the official documentation:
https://docs.scrapy.org/en/latest/topics/items.html
"""

from scrapy import Field, Item


class BankItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    url = Field()
    bank_name = Field()
    rating = Field()
    # pass



