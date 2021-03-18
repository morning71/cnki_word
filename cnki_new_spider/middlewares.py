# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


from scrapy import signals
from fake_useragent import UserAgent
import datetime
import random
import requests
import datetime


class CnkiNewSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BaiduSpiderProxyIPDownloadMiddleware(object):
    def __init__(self):
        # self.url = 'http://www.xiongmaodaili.com/xiongmao-web/api/glip?secret=3444673712b38f300e4a4a8f5f11cd54&orderNo=GL20190812135154803i8gg7&count=1&isTxt=1&proxyType=1'
        # self.url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=0&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions='
        # self.url = 'http://www.xiongmaodaili.com/xiongmao-web/api/glip?secret=3444673712b38f300e4a4a8f5f11cd54&orderNo=GL20191009010447RVl0Nap3&count=1&isTxt=1&proxyType=1'
        self.url = 'http://www.xiongmaodaili.com/xiongmao-web/api/glip?secret=3444673712b38f300e4a4a8f5f11cd54&orderNo=GL20200927233750fHgLFdut&count=1&isTxt=1&proxyType=1'
        # self.url = 'http://kuyukuyu.com/api/projects/get?uuid=4363edc5-8c07-4f6b-a5fc-215f23f7eb12'
        self.proxy = ''
        self.expire_datetime = datetime.datetime.now() - datetime.timedelta(seconds=10)
        # self._get_proxyip()

    def _get_proxyip(self):
        resp = requests.get(self.url)
        info = resp.text.split('\n')
        proxy = info[0]
        print('------当前使用----:',proxy)
        self.proxy = proxy
        self.expire_datetime = datetime.datetime.now() + datetime.timedelta(seconds=10)

    def _check_expire(self):
        if datetime.datetime.now() >= self.expire_datetime:
            self._get_proxyip()
            print('======*'*4,'ip已切换：'+self.proxy)

    def process_request(self,spider,request):
        self._check_expire()
        request.meta['proxy'] = 'http://'+self.proxy


import base64

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H2190R3707TZ51GD"
proxyPass = "7EAA5CF92B387D3B"

# # for Python2
# proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)

# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth