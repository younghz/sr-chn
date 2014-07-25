# -*-coding:utf-8 -*-

#整体分析：在配置文件中的两部分(1)scrapy_redis.scheduler.Scheduler和
#（2）scrapy_redis.pipelines.RedisPipeline实现分布式功能。

#分布式爬取是通过（1）实现，可以实例多个spider共享redis队列中的request
#分布式item处理是通过（2）实现。

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

#限制爬取深度，以便观察request的从business到game的转换
DEPTH_LIMIT = 1

DOWNLOAD_DELAY = 2
#调度器
#这里是使能调度器，将request存储到redis queue中

#默认是使用scrapy.core.scheduler.Scheduler，现在使用scrapy_redis中实现的调度器。
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#不清空redis queue，允许爬取过程中暂停并恢复
SCHEDULER_PERSIST = True
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

#在spider中得到的item会最终传到itempipline中处理，而这里设置的就是启动的pipline
#其中第一个是自己实现的pipeline,第二个是scrapy_redis实现的pipeline

#而后者对item的处理是：“将serialized item数据push进一个redis list/queue中”
ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}
