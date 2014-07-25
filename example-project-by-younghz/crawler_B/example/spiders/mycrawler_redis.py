# -*-coding:utf-8-*-

from scrapy_redis.spiders import RedisMixin

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from example.items import ExampleLoader


class MyCrawler(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls).

    定义从redis queue中读取url的spider。
    这个redis queue的名字就是下方定义的redis_key。

    这个不同于一般的spider，像dmoz。dmoz是在redis实现的scheduler中获得request。
    而这种是在自建的redis queue中获得url。这个url就像redis_key中定义的是一种类似与
    正常在spider中编写的start_url的作用。
    """
    name = 'mycrawler_redis'
    #这是在RedisMixin中定义的变量
    redis_key = 'mycrawler:start_urls'

    rules = (
        # follow all links
        Rule(SgmlLinkExtractor(), callback='parse_page', follow=True),
    )

    #这是对CrawlSpider中的set_crawler的重新实现。
    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        #安装redis连接和设置idle signal。
        #并且这个函数必须在spider设置特的crawler object（上面的函数）之后调用。
        RedisMixin.setup_redis(self)

    def parse_page(self, response):
        el = ExampleLoader(response=response)
        el.add_xpath('name', '//title[1]/text()')
        el.add_value('url', response.url)
        return el.load_item()
