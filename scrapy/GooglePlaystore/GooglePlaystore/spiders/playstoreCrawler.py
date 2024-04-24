import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from GooglePlaystore.items import GoogleplaystoreItem, GoogleplaystoreDevItem

class CrawlingSpider(CrawlSpider):
    name = 'playcrawler'
    allowed_domains = ['google.com']

    custom_settings = {
        # 'FEEDS': {'data.csv': {'format': 'csv'},},
        'FEEDS': {'output.jsonl': {'format': 'jsonlines'},},
    }

    rules = (
        Rule(LinkExtractor(allow='/store/apps/developer'), callback="parse_item"),
        # Rule(LinkExtractor(allow="/store/apps/details")),
    )

    def start_requests(self):
        url = 'https://play.google.com/store/apps/details?id=com.whatsapp'
        yield scrapy.Request(url, callback=self.parse, meta={'source_url': url},)

        # empty the output file first
        open("output.jsonl", 'w').close()


    def parse(self, response):
        product = response.css('div.tU8Y5c')
        Playstore_item = GoogleplaystoreItem()
        
        Playstore_item['app'] = product.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/text()').get(),

        Playstore_item['app_link'] = response.meta.get('source_url')

        Playstore_item['organization_name'] = product.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div/a/span/text()').get(),

        Playstore_item['organization_link'] = product.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div/a/@href').get()
        Playstore_item['organization_link'] = 'https://play.google.com' + Playstore_item['organization_link']

        Playstore_item['website'] = product.xpath('//*[@id="developer-contacts"]/div/div[1]/div/a/@href').get(),

        Playstore_item['support_email'] = product.xpath('//*[@id="developer-contacts"]/div/div[2]/div/a/div/div[2]/text()').get(),
        
        Playstore_item['app_purchase'] = product.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div[2]/div/span/text()').get(),


        yield Playstore_item



        organization_link = Playstore_item['organization_link']
        yield response.follow(organization_link, callback=self.parse_organization)
    
    def parse_organization(self, response):     
 
        related_products = response.css('.VfPpkd-aGsRMb')
        developer_items = GoogleplaystoreDevItem()

        for product in related_products:             
            developer_items['product'] = product.css('span.DdYX5::text').get()

            developer_items['product_link'] = product.css('a.Si6A0c.Gy4nib::attr(href)').get()
            developer_items['product_link'] = 'https://play.google.com' + developer_items['product_link']

            developer_items['rating'] = product.css('span.w2kbF::text').get()

            developer_items['organization_name'] = product.css('span.wMUdtb::text').get()

            yield developer_items






























            # developer_items['product'] = product.xpath('//*[@id="yDmH0d"]/c-wiz[3]/div/div/div[1]/c-wiz/c-wiz/c-wiz/section/div/div/div/div[1]/div/div/div/a/div[2]/div/div[1]/span/text()').get(),

            # developer_items['rating'] = product.xpath('//*[@id="yDmH0d"]/c-wiz[3]/div/div/div[1]/c-wiz/c-wiz/c-wiz/section/div/div/div/div[1]/div/div/div/a/div[2]/div/div[3]/div/span[1]/text()').get(),
        
            # developer_items['organization_link'] = product.xpath('//*[@id="yDmH0d"]/c-wiz[3]/div/div/div[1]/c-wiz/c-wiz/c-wiz/section/div/div/div/div[1]/div/div/div/a/div[2]/div/div[2]/span/text()').get(),


        



        # yield {
        #     "app": response.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/text()').get(),
        #     "organization": response.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div/a/span/text()').get(),
        #     "website": response.xpath('//*[@id="developer-contacts"]/div/div[1]/div/a/@href').get(),
        #     "support email": response.xpath('//*[@id="developer-contacts"]/div/div[2]/div/a/div/div[2]/text()').get(),
        #     }


        

            # "app": response.css('h1.Fd93Bb F5UCq xwcR9d::text').get(),
            # "organization": response.css('div.Vbfug auoIOc::text').get(),
            # "website": response.css('div.VfPpkd-EScbFb-JIbuQc  a::attrs(href)').get(),
            # "support email": response.css('div.pSEeg::text').get(),


    # def parse(self, response):
    #     path = response.url.split("/")[-1]
    #     page = response.path.split("=")[-1]
    #     filename = f"{page}.html"
    #     Path(filename).write_bytes(response.body)
    #     self.log(f"Saved file {filename}")




