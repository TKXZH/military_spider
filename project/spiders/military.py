from datetime import datetime, timedelta

import scrapy


class Military(scrapy.Spider):
    site_map = {
        'aircraft': 'https://www.militaryfactory.com/aircraft/aircraft-by-country.asp',
        'ships': 'https://www.militaryfactory.com/ships/navy-warships-and-submarines-by-country.asp',
        'armor': 'https://www.militaryfactory.com/armor/land-systems-by-country.asp',
        'gun': 'https://www.militaryfactory.com/smallarms/guns-by-country.asp'
    }
    name = 'military_spider'
    custom_settings = {
        "FEED_FORMAT": 'csv',
        "FEED_URI": "data/%(bjtime)s/%(category)s/data.csv",
        "ITEM_PIPELINES": {'project.pipelines.MilitaryImagePipeline': 1},
        "IMAGES_STORE": "data/images"
    }

    def __init__(self, category=None, *args, **kwargs):
        if category in self.site_map:
            self.start_urls = [self.site_map[category]]
            self.category = category
            now_time = datetime.now()
            beijing_time = now_time - timedelta(hours=8)
            beijing_time_str = beijing_time.strftime("%Y%m%d%H%M%S")
            self.bjtime = beijing_time_str
        else:
            raise Exception('no mapping for category!')
        super(Military, self).__init__(*args, **kwargs)

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
            "detail": '\n'.join(response.xpath("//span[@class='textLarge textDkGray']/text()").getall()),
            "desc": response.xpath("(//span[@class='textLarge textWhite'])[1]/text()").get(),
            "image_urls": list(map(response.urljoin, response.xpath("//img[contains(@data-u,'image')]/@src").getall()))
        }
        buttons = response.xpath("(//button[@class='collapsible'])")
        for button in buttons:
            button_name = button.xpath("text()").get()
            names = button.xpath(
                "following-sibling::div[1]//span[@class='textLarge textYellow textBold']/text()").getall()
            values = button.xpath("following-sibling::div[1]//span[@class='textLarge textWhite']/text()").getall()
            if len(names) != 0:
                detail.update(dict(zip(names, values)))
            else:
                direct_str = ','.join(
                    button.xpath("following-sibling::div[1]//span[contains(@class,'textWhite')]/text()").getall())
                detail[button_name] = direct_str

        yield {k: v.strip() if type(v) is str else v for k, v in detail.items()}
