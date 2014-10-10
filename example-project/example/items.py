#-*-coding:utf-8-*-

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
#ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Join

#定义存储item
class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()


#继承自ItemLoader的类，ItemLoader API比Item自带API更便捷，对于填充items
#这里的流程是这样的：目的是处理ExampleItem，首先将得到的字段经过输入处理器处理，然后
#经由输出处理器处理。最后得到处理后的ExampleItem。
class ExampleLoader(ItemLoader):
    #定义默认处理的Item为上方定义的ExampleItem
    default_item_class = ExampleItem
    #定义默认输入处理器和输出处理器
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
