# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlaystoreappsItem(scrapy.Item):
    # define the fields for your item here like:
    app_name = scrapy.Field()
    app_link = scrapy.Field()
    org_name = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    developer_page_link = scrapy.Field()

class OrganizationItem(scrapy.Item):
    org_link = scrapy.Field()
    # main_app_name = scrapy.Field()
    dev_app_name = scrapy.Field()
    dev_app_link = scrapy.Field()
    dev_app_org_name = scrapy.Field()
    dev_app_rating = scrapy.Field()
