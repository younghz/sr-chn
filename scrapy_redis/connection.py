#-*-coding:utf-8-*-

import redis


# Default values.
REDIS_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

#调用时参数setting=crawler.setting,这样可以就可以通过获得访问字典的方式获得在setting.py中设置的参数值
def from_settings(settings):
    url = settings.get('REDIS_URL',  REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)

    # REDIS_URL 较 host/port 有更高的优先级.返回的是redis客户端连接实例
    if url:
        return redis.from_url(url)
    else:
        return redis.Redis(host=host, port=port)
