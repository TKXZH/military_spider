# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline


class ProjectPipeline(object):
    def process_item(self, item, spider):
        return item


class MilitaryImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if len(results) > 0:
            image_paths = [x['path'] for ok, x in results if ok]
            if image_paths:
                item['image_paths'] = ','.join(image_paths)
                return item
        else:
            return item
