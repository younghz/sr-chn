#-*-coding:utf-8-*-

import time
import connection

from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class RFPDupeFilter(BaseDupeFilter):
    """基于redis的request去重过滤器"""

    def __init__(self, server, key):
        """初始化 duplication filter

        Parameters
        ----------
        server : Redis instance
        key : str
            存储fingerprints
        """
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        server = connection.from_settings(settings)
        # create one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    #使用set结构存储request的fingerprint,利用set结构的value唯一不能重复的特性，使相同request的fingerprint无法插入到其中
    #从而达到去重过滤的效果

    #插入成功返回0,相当与not seen
    def request_seen(self, request):
        #来自scrapy.utils.request的request_fingerprint函数接受request参数并返回fingerprint
        fp = request_fingerprint(request)
        added = self.server.sadd(self.key, fp)
        return not added

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """清空redis key中存储的 fingerprints data"""
        self.server.delete(self.key)
