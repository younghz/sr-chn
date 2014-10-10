说在前面
========

此repository fork自scrapy-redis，在此基础上，做了如下更改：

* 重写部分代码，与更新版本的scrapy兼容。
* 更清晰的展现分布式例程的实现。
* 用法的翻译/代码原理研究/注释翻译。

注意：部分兼容性问题存在于此库中，关于此方面问题可直接查看源代码库 (github.com/darkrho/scrapy-redis)或者 (github.com/younghz/scrapy-redis)。

新例程原理与使用
================

关于新例程 "example-project-by-younghz" 实现 **原理** 和 **使用** 请参见本repo的wiki，
或者查看我的这篇文章（http://blog.csdn.net/u012150179/article/details/38091411）。在例程文件夹下也有README文件。

最近有人发邮件问我相关问题，在上面指出的文章中都有详细说明。

Redis-based components for Scrapy
=================================

This project attempts to provide Redis-backed components for Scrapy.

Features:

* 分布式爬取/抓取
    可以同时实例化多个spider，它们使用同一个redis队列（request queue）。
    适合广度多域名的抓取。
* 分布式post-processing（处理得到的item）
    可以将抓取的item放进redis队列中，这样你就可以在需要的时候在item队列中进行处理。

Requirements:

* Scrapy >= 0.14
* redis-py (tested on 2.4.9)
* redis server (tested on 2.4-2.6)

Available Scrapy components:

* Scheduler
* Duplication Filter
* Item Pipeline
* Base Spider


Installation
------------

From `pypi`::

  $ pip install scrapy-redis

From `github`::

  $ git clone https://github.com/darkrho/scrapy-redis.git
  $ cd scrapy-redis
  $ python setup.py install


使用
-----

Enable the components in your `settings.py`:

.. code-block:: python

  # Enables scheduling storing requests queue in redis.
  SCHEDULER = "scrapy_redis.scheduler.Scheduler"

  # Don't cleanup redis queues, allows to pause/resume crawls.
  SCHEDULER_PERSIST = True

  # Schedule requests using a priority queue. (default)
  SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

  # Schedule requests using a queue (FIFO).
  SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

  # Schedule requests using a stack (LIFO).
  SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

  # Max idle time to prevent the spider from being closed when distributed crawling.
  # This only works if queue class is SpiderQueue or SpiderStack,
  # and may also block the same time when your spider start at the first time (because the queue is empty).
  SCHEDULER_IDLE_BEFORE_CLOSE = 10

  # Store scraped item in redis for post-processing.
  ITEM_PIPELINES = [
      'scrapy_redis.pipelines.RedisPipeline',
  ]
  
  # Specify the host and port to use when connecting to Redis (optional).
  REDIS_HOST = 'localhost'
  REDIS_PORT = 6379
  
  # Specify the full Redis URL for connecting (optional).
  # If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
  REDIS_URL = 'redis://user:pass@hostname:9001'

.. note::

  Version 0.3 changed the requests serialization from `marshal` to `cPickle`,
  therefore persisted requests using version 0.2 will not able to work on 0.3.


Running the example project
---------------------------

这个例子所表现的是多个crawler怎样使用一个spider的request queue。

1. 安装scrapy-redis。

2. 运行crawler然后停止::

    $ cd example-project
    $ scrapy crawl dmoz
    ... [dmoz] ...
    ^C

3. 再次运行crawler从上次停止位置恢复::

    $ scrapy crawl dmoz
    ... [dmoz] DEBUG: Resuming crawl (9019 requests scheduled)

4. 运行更多的scrapy crawlers::

    $ scrapy crawl dmoz
    ... [dmoz] DEBUG: Resuming crawl (8712 requests scheduled)

5. 运行一个或更多的post-processing workers::

    $ python process_items.py
    Processing: Kilani Giftware (http://www.dmoz.org/Computers/Shopping/Gifts/)
    Processing: NinjaGizmos.com (http://www.dmoz.org/Computers/Shopping/Gifts/)
    ...


Feeding a spider from Redis
---------------------------

`scrapy_redis.spiders.RedisSpider`类可以使spider从redis中读取urls，
redis queue中的urls会被依次处理，如果第一个request yeilds更多的request，
那么spider会首先处理这些request,然后在从redis fetch 另外的url。

For example, create a file `myspider.py` with the code below:

.. code-block:: python

    from scrapy_redis.spiders import RedisSpider

    class MySpider(RedisSpider):
        name = 'myspider'

        def parse(self, response):
            # do stuff
            pass


然后:

1. 运行spider::

    scrapy runspider myspider.py

2. push urls to redis::

    redis-cli lpush myspider:start_urls http://google.com


Changelog
---------

0.5
  * Added `REDIS_URL` setting to support Redis connection string.
  * Added `SCHEDULER_IDLE_BEFORE_CLOSE` setting to prevent the spider closing too
    quickly when the queue is empty. Default value is zero keeping the previous
    behavior.

0.4
  * Added `RedisSpider` and `RedisMixin` classes as building blocks for spiders
    to be fed through a redis queue.
  * Added redis queue stats.
  * Let the encoder handle the item as it comes instead converting it to a dict.

0.3
  * Added support for different queue classes.
  * Changed requests serialization from `marshal` to `cPickle`.

0.2
  * Improved backward compatibility.
  * Added example project.

0.1
  * Initial version.


.. image:: https://d2weczhvl823v0.cloudfront.net/darkrho/scrapy-redis/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

