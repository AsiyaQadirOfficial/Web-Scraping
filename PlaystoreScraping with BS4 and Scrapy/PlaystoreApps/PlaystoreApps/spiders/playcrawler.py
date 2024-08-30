import scrapy
import requests
import os
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from PlaystoreApps.items import PlaystoreappsItem, OrganizationItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class PlaycrawlerSpider(CrawlSpider):
    name = "playcrawler"
    allowed_domains = ["play.google.com"]
    start_urls = []

    query = 'Editors'
    url = f"https://play.google.com/store/search?q={query}&c=apps"
    

    custom_settings = {
        # 'FEEDS': {f'{query}/test-file-%(time)s.json': {'format': 'json'}},
        # Use Feed Exports to save items into separate files based on item class
        'FEEDS': {
            f'{query}/app_details.json': {
                'format': 'json',
                'overwrite': True,
                'item_classes': ['PlaystoreApps.items.PlaystoreappsItem'],  # Ensure only PlaystoreappsItem goes here
            },
            f'{query}/developers.json': {
                'format': 'json',
                'overwrite': True,
                'item_classes': ['PlaystoreApps.items.OrganizationItem'],  # Ensure only OrganizationItem goes here
            },
        }
    }
    
    rules = (
        Rule(LinkExtractor(allow='store/apps/details'), callback="parse_app"),
        Rule(LinkExtractor(allow=r'store/apps/(developer|dev)'), callback="parse_organization", follow=True),
    )


    # ---------------------------- STARTING POINT ----------------------------------------

    html_content = requests.get(url)
    soup = BeautifulSoup(html_content.text, 'html.parser')
    # print(soup.prettify())
    
    os.makedirs(query, exist_ok=True)
    with open(f"{query}/{query}.html", "w+", encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    with open(f"{query}/{query}.html", "r+", encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser') 
        app_links = soup.find_all('a', class_='Si6A0c Gy4nib')
        # print(app_links)
        for app_link in app_links:
            link = app_link.get('href')
            link = 'https://play.google.com' + link 
            if link:
                start_urls.append(link)
        else:
            print('Link not found')

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_app, 
                errback=self.errback_httpbin)
            
    def parse_app(self, response):
        self.logger.info("Parse function called on %s", response.url)
        current_url = response.url

        item = PlaystoreappsItem()

        app_name = response.css('h1.Fd93Bb.F5UCq.p5VxAd::text')
        if app_name:
            item['app_name'] = app_name.get()
        else:
            app_name = response.css('h1.Fd93Bb.F5UCq.xwcR9d::text')
            if app_name:
                item['app_name'] = app_name.get()
            else:
                app_name = response.css('h1.Fd93Bb.ynrBgc.xwcR9d::text')
                if app_name:
                    item['app_name'] = app_name.get()
                else:
                    app_name = 'Not Found!'

        item['app_link'] = current_url
        
        item['org_name'] = response.css('div.Vbfug.auoIOc span::text').get()
        
        item['rating'] = response.css('div.TT9eCd::text').get()

        item['reviews'] = response.css('div.g1rdde::text').get()

        item['website'] = response.css('a.Si6A0c.RrSxVb::attr(href)').get()

        email = response.xpath('//*[@id="developer-contacts"]/div/div[2]/div/a/div/div[2]/text()').get()
        if email:
            item['email'] = email
        else:
            email = response.xpath('//*[@id="developer-contacts"]/div/div[1]/div/a/div/div[2]/text()').get()
            if email:
                item['email'] = email 
            else:
                item['email'] = response.xpath('//*[@id="developer-contacts"]/div/div[3]/div/a/div/div[2]/text()').get()


        developer_page_link = response.css('div.Vbfug.auoIOc a::attr(href)').get()
        if developer_page_link:
            developer_page_link = 'https://play.google.com' + developer_page_link
            item['developer_page_link'] = developer_page_link

        yield item 
    

        if developer_page_link:
            yield response.follow(developer_page_link, callback=self.parse_organization, cb_kwargs={'main_app_name': item['app_name']})        #cb_kwargs: Used to pass the main app details to the parse_organization method for linking related apps back to their main app.
                       

    def parse_organization(self, response, main_app_name):

        related_products = response.css('.VfPpkd-EScbFb-JIbuQc')
        for product in related_products: 
            organization = OrganizationItem()

            organization['org_link'] = response.url
            # organization['main_app_name'] = main_app_name


            # dev_app_org_name = product.css('div.q7T63c::text()').get()
            # if dev_app_org_name:
            #     organization['dev_app_org_name'] = dev_app_org_name
            # else:
            #     dev_app_org_name = product.css('div.LbQbAe::text()').get()
            #     if dev_app_org_name:
            #         organization['dev_app_org_name'] = dev_app_org_name
            #     else:
            #         dev_app_org_name = product.css('div.wMUdtb::text()').get()
            #         if dev_app_org_name:
            #             organization['dev_app_org_name'] = dev_app_org_name
            #         else:
            #             dev_app_org_name = 'Not Found!'

            dev_app_org_name = product.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/c-wiz/c-wiz/section/div/div/div/div[1]/div/div[1]/div/a/div[2]/div/div[2]/span/text()').get()
            if dev_app_org_name:
                organization['dev_app_org_name'] = dev_app_org_name
            else:
                dev_app_org_name = product.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div/div[1]/div/h1/div/text()').get()
                if dev_app_org_name:
                    organization['dev_app_org_name'] = dev_app_org_name
                else:
                    dev_app_org_name = product.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[2]/div[1]/c-wiz/c-wiz/c-wiz/section/div/div/div[1]/div[1]/div[1]/div/div[2]/text()').get()
                    if dev_app_org_name:
                        organization['dev_app_org_name'] = dev_app_org_name 
                    else:
                        dev_app_org_name = 'Not Found!'


            dev_app_name =  product.css('span.DdYX5::text').get()
            if dev_app_name:
                organization['dev_app_name'] = dev_app_name
            else:
                dev_app_name = product.css('div.Epkrse::text').get()
                if dev_app_name:
                    organization['dev_app_name'] = dev_app_name
                else:
                    dev_app_name = 'Not Found!'



            dev_app_link =  product.css('a.Si6A0c.Gy4nib::attr(href)').get()
            if dev_app_link:
                organization['dev_app_link'] = dev_app_link
            else:
                dev_app_link = product.css('a.Si6A0c.ZD8Cqc::attr(href)').get()
                if dev_app_link:
                    organization['dev_app_link'] = dev_app_link
                else:
                    dev_app_link = 'Not Found!'



            dev_app_rating =  product.css('span.w2kbF::text').get()
            if dev_app_rating:
                organization['dev_app_rating'] = dev_app_rating
            else:
                dev_app_rating = product.css('div.LrNMN::text').get()
                if dev_app_rating:
                    organization['dev_app_rating'] = dev_app_rating 
                else:
                    dev_app_rating = 'Not Found!'


            yield organization

        
    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f"HttpError on {response.url}")

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error(f"DNSLookupError on {request.url}")

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(f"TimeoutError on {request.url}")            
