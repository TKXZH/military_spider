from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.military import Military

settings = get_project_settings()
process = CrawlerProcess(get_project_settings())
process.crawl(Military, category='aircraft')

if __name__ == '__main__':
    process.start()
