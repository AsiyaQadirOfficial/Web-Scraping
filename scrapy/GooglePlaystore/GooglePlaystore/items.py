# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy.item import Item, Field

class GoogleplaystoreItem(scrapy.Item):
    # define the fields for your item here like:
    app = scrapy.Field()
    app_link = scrapy.Field()
    organization_name = scrapy.Field()
    organization_link = scrapy.Field()
    website = scrapy.Field()
    support_email = scrapy.Field()
    app_purchase = scrapy.Field()
    
class GoogleplaystoreDevItem(scrapy.Item):
    # define the fields for your item here like:
    product = scrapy.Field()
    product_link = scrapy.Field()
    rating = scrapy.Field()
    organization_name = scrapy.Field()