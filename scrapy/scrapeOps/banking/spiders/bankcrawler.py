import scrapy
# from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from banking.items import BankingItem, OrganizationItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class BankcrawlerSpider(scrapy.Spider):
    name = "mycrawler"
    allowed_domains = ["play.google.com"]

    query = "banking apps pakistan"
    start_urls = [f"https://play.google.com/store/search?q={query}&c=apps"]

    # rules = (
    #     Rule(LinkExtractor(allow='store/apps/details'), callback="parse_app", follow=True),
    #     Rule(LinkExtractor(allow=r'store/apps/(developer|dev)'), callback="parse_organization", follow=True),
    # )

    custom_settings = {
        'FEEDS': {'Output/test-file-%(time)s.json': {'format': 'json'}},
        # 'FEEDS': {'Output/test-file-%(time)s.csv': {'format': 'csv'}},
        }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_start_page, 
                # cb_kwargs={},
                errback=self.errback_httpbin)
            

    def parse_start_page(self, response):
        # flex = response.xpath('//div[@class="ftgkle"]')
        apps = response.xpath('//div[@class="ULeU3b"]')
        for app in apps:
            app_link = app.xpath('.//a/@href').get()
            if app_link:
                yield response.follow(app_link, callback=self.parse_app)


    def parse_app(self, response):
        self.logger.info("Parse function called on %s", response.url)
        current_url = response.url

        items = response.css('.tU8Y5c')
        for item in items: 
            banking = BankingItem()
            
            banking['app_name'] = item.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/text()').get()

            banking['org_name'] = item.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div/a/span/text()').get()
            
            banking['app_link'] = current_url

            banking['rating'] = item.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[1]/div[1]/div/div/text()').get()

            banking['website'] = item.xpath('//*[@id="developer-contacts"]/div/div[1]/div/a/@href').get()

            developer_page_link = item.css('div.Vbfug.auoIOc a::attr(href)').get()
            if developer_page_link:
                developer_page_link = 'https://play.google.com' + developer_page_link
            banking['developer_page_link'] = developer_page_link

            email = item.xpath('//*[@id="developer-contacts"]/div/div[2]/div/a/div/div[2]/text()').get()
            if email:
                banking['email'] = email
            else:
                email = item.xpath('//*[@id="developer-contacts"]/div/div[1]/div/a/div/div[2]/text()').get()
                if email:
                    banking['email'] = email 
                else:
                    banking['email'] = item.xpath('//*[@id="developer-contacts"]/div/div[3]/div/a/div/div[2]/text()').get()

            yield banking 

        if developer_page_link:
            yield response.follow(developer_page_link, callback=self.parse_organization,  cb_kwargs={'main_app_name': banking['app_name']})        

            # yield response.follow(developer_page_link, callback=self.parse_organization, cb_kwargs={'main_app': banking})                       #cb_kwargs: Used to pass the main app details to the parse_organization method for linking related apps back to their main app.


    def parse_organization(self, response, main_app_name):
        related_products = response.css('.VfPpkd-EScbFb-JIbuQc')
        # VfPpkd-EScbFb-JIbuQc UVEnyf
        for product in related_products: 
            organization = OrganizationItem()

            organization['org_link'] = response.url
            organization['main_app_name'] = main_app_name

            related_app_org_name = product.css('span.wMUdtb::text').get()
            if related_app_org_name:
                organization['related_app_org_name'] = related_app_org_name
            else:
                # organization['related_app_org_name'] = product.css('div.XcQm1d h1::text').get()
                organization['related_app_org_name'] = product.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div/div[1]/div/h1/div/text()').get()


            related_app_name =  product.css('span.DdYX5::text').get()
            if related_app_name:
                organization['related_app_name'] = related_app_name
            else:
                organization['related_app_name'] = product.css('div.Epkrse::text').get()


            related_app_rating =  product.css('span.w2kbF::text').get()
            if related_app_rating:
                organization['related_app_rating'] = related_app_rating
            else:
                organization['related_app_rating'] = product.css('div.LrNMN::text').get()

            yield organization
            

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):

            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError on %s", request.url)