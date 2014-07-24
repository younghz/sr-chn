#-*-coding:utf-8-*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

class ExamplePipeline(object):
    def process_item(self, item, spider):
        #将spider中没有赋值的字段赋值，这也就是pipeline的作用：进一步处理item
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item
