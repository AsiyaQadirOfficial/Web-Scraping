# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BankingItem(scrapy.Item):
    # define the fields for your item here like:
    app_name = scrapy.Field()
    org_name = scrapy.Field()
    rating = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    app_link = scrapy.Field()
    developer_page_link = scrapy.Field()
    related_app_org_name = scrapy.Field()
    org_link = scrapy.Field()
    related_app_name = scrapy.Field()
    related_app_rating = scrapy.Field()
    
class OrganizationItem(scrapy.Item):
    org_link = scrapy.Field()
    related_app_org_name = scrapy.Field()
    related_app_name = scrapy.Field()
    related_app_rating = scrapy.Field()
    main_app_name = scrapy.Field()