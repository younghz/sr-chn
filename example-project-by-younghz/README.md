## 一 Scrapy-redis实现分布式爬取分析
所谓的scrapy-redis实际上就是scrapy+redis，其中对redis的操作采用redis-py客户端。这里的redis的作用以及scrapy-redis的在自己fork的repository 已经做了解释或翻译（README.rst）。    
在前面一篇文章中我已经借助两篇相关文章分析了使用redis实现爬虫分布式的中心。归结起来就是：所有爬虫获取到的url(request)都放到一个redis queue中，并且所有爬虫都从单个redis queue中获取request(url)。    
scrapy-redis已经很长时间没有更新，如何是它兼容更新版本的scrapy我在博文（链接：[http://blog.csdn.net/u012150179/article/details/38087661](http://blog.csdn.net/u012150179/article/details/38087661)）中也已经说明。

## 二 分布式爬取实现
#### 1. 对scrapy-redis中自带example的分析
在库的README中已经对example的使用做了说明，但是初步接触时运行example中的spider会存在很多疑问，比如，分布式体现在哪？是通过那几方面实现的？其次，在运行结果中很难发现分布式的影子，感觉就像两个spider在自己爬自己的东西。
对于第一种疑问，我在翻译和标注scrapy-redis中settings.py已经做了说明。而第二中疑问也是实现2中自己的example所要做的。

#### 2. 更清晰验证scrapy-redis实现分布式的思路与编码实现。
#####（1）思路
实现两个爬虫，定义爬虫A爬取dmoz.com的关键词bussiness下的所有链接（通过start_urls设定）。爬虫B爬取game下的所有链接，观察二者同时运行时爬取链接的url，是各自范围的url还是二者的交集。这样由于二者定义的爬取范围是不一致的，通过爬取现象可以得出结果。
#####（2）实现
代码放在了github的repo中（https://github.com/younghz/scrapy-redis/）。为了易于观察，设置DEPTH_LIMIT为1。
#####（3）现象与分析
现象：可以发现，二者是首先同时爬取单个关键词下的链接（首先爬取哪一个取决与先运行爬虫的start_urls），完毕后进而爬取另一个关键词下链接。
分析：通过同时爬取单个关键词可以说明两个爬虫是同时被调度的，这就是爬虫的分布式。并且爬虫默认是广度优先搜索的。爬取的步骤如下：

i)**首先**运行爬虫A（B同理），爬虫引擎请求spider A中start_urls中的链接并交割调度器，进而引擎向调度器请求爬取的url并交给下载器下载,下载后的response交给spider,spider根据定义的rules得到链接，继续通过引擎交给调度器。（这一系列过程可查看scrapy架构）。其中调度器scheduler中request（url）顺序是redis queue实现的，也就是将request(url)push到queue中，请求时pop出来。

ii)**进而**启动B，同理B的start_urls首先交给了调度器（注意和A中的调度器是同一个），而B的引擎请求爬取url时，调度器调度给B下载的url还是A中没下载完成的url（默认的调度方式是先调度返回的url,并且是广度优先的），这是A和B同时下载A中未完成链接，待完成后，同时下载B的要求链接。

iii)**问题**：上述ii中的调度方式是怎样实现的？
在scrapy-redis中默认使用的是SpiderPriorityQueue方式，这是由sorted set实现的一种非FIFO、LIFO方式。
#### 3. 细节分析与注意点
每次执行重新爬取，应该将redis中存储的数据清空，否则影响爬取现象。

