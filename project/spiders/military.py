import scrapy
import re


class Military(scrapy.Spider):
    start_urls = ['https://www.militaryfactory.com/smallarms/guns-by-country.asp']

    custom_settings = {
        "FEED_URI": 'exported_data/%(name)s/%(time)s.csv',
        "FEED_FORMAT": 'csv'
    }

    def parse(self, response):
        a = self.settings
        urls = response.xpath("(//div[@class='contentStripInner'])[4]//a/@href")
        for url in urls:
            yield response.follow(url, self.handle_list)

    def handle_list(self, response):
        items = response.xpath("//div[@class='box']//a/@href")
        for item in items:
            yield response.follow(item, self.extract_detail)

    def extract_detail(self, response):
        detail = {
            "url": response.request.url,
            "name": response.xpath("//h1/text()").get(),
            "detail": response.xpath("//span[@class='textLarge textDkGray']/text()").getall(),
            "desc": response.xpath("(//span[@class='textLarge textWhite'])[1]/text()").get(),
            "year": response.xpath("(//span[@class='textLarge textWhite'])[2]/text()").get(),
            "manufacturing": response.xpath("(//span[@class='textLarge textWhite'])[3]/text()").get(),
            "operators": response.xpath("(//span[@class='textLarge textWhite'])[4]/text()").get(),
            "roles": response.xpath("(//span[@class='textLarge textWhite'])[5]/text()").get(),
            "overall_length": response.xpath("(//span[@class='textLarge textWhite'])[6]/text()").get(),
            "barrel_length": response.xpath("(//span[@class='textLarge textWhite'])[7]/text()").get(),
            "weight": response.xpath("(//span[@class='textLarge textWhite'])[8]/text()").get(),
            "sights": response.xpath("(//span[@class='textLarge textWhite'])[9]/text()").get(),
            "action": response.xpath("(//span[@class='textLarge textWhite'])[10]/text()").get(),
            "muzzle_velocity": response.xpath("(//span[@class='textLarge textWhite'])[11]/text()").get(),
            "rate_od_fire": response.xpath("(//span[@class='textLarge textWhite'])[12]/text()").get(),
        }
        yield {k: v.strip() if type(v) is str else v for k, v in detail.items()}
