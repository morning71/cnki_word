# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 14:31
# @Author  : Morning-J
# @FileName: cnki_new_spider.py
# @Software: PyCharm
# @Github:morning71
import scrapy
import logging
import pymysql
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from cnki_new_spider.items import CnkiNewSpiderItem

class CnkiNewSpider(scrapy.spiders.Spider):
    MAX_RETRY = 10
    logger = logging.getLogger(__name__)
    name = 'cnki_new_spider'
    db = pymysql.connect('localhost','root','morning321','cnki_new')
    cursor = db.cursor()
    select_sql = 'SELECT key_word FROM search_word_p WHERE key_word NOT IN (SELECT key_word FROM t_cnki_new_8);'
    cursor.execute(select_sql)
    res = cursor.fetchall()
    start_url = []
    for i in res:
        start_url.append(i[0])

    def start_requests(self):
        for i in self.start_url:
            key_word = i
            meta = {'key_word':key_word}
            data = {"queryJson":{"Platform": "",
                    "DBCode": "CFLS",
                    "KuaKuCode": "CJFQ,CDMD,CIPD,CCND,CISD,SNAD,BDZK,CCVD,CJFN,CCJD",
                        "QNode": {"QGroup":
                                      [
                                        {"Key": "Subject",
                                        "Title": "",
                                        "Logic": 1,
                                        "Items":
                                             [
                                            {"Title": "主题",
                                             "Name": "SU",
                                             "Value": key_word,
                                             "Operate": "%=",
                                             "BlurType": ""}
                                        ],
                                        "ChildItems": []}]
                        }
                    }}
            # data = "queryJson=%7B%22Platform%22%3A%22%22%2C%22DBCode%22%3A%22CFLS%22%2C%22KuaKuCode%22%3A%22CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCVD%2CCJFN%2CCCJD%22%2C%22QNode%22%3A%7B%22QGroup%22%3A%5B%7B%22Key%22%3A%22Subject%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A1%2C%22Items%22%3A%5B%7B%22Title%22%3A%22%E4%B8%BB%E9%A2%98%22%2C%22Name%22%3A%22SU%22%2C%22Value%22%3A%22%E7%94%9F%E7%89%A9%E6%9F%B4%E6%B2%B9%22%2C%22Operate%22%3A%22%25%3D%22%2C%22BlurType%22%3A%22%22%7D%5D%2C%22ChildItems%22%3A%5B%5D%7D%5D%7D%7D"
            url = 'https://kns.cnki.net/KNS8/Group/Result'
            headers = {'Content-Type':'application/x-www-form-urlencoded',
                       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                       'Referer':'https://kns.cnki.net/KNS8/Group/Result'}
            yield scrapy.Request(url,method='POST',body=urlencode(data),headers=headers,meta=meta,callback=self.list_html)
            # yield scrapy.FormRequest(url,formdata=json.dumps(data),headers=headers,meta=meta,callback=self.list_html)
    def list_html(self,response):
        html = response.body.decode('utf-8')
        # print(response.meta['key_word'])
        # print('**********')
        # print(html)
        # print('**********')
        soup = BeautifulSoup(html,'lxml')
        primary_word = []
        secondary_word = []
        #主要主题
        primary_topic = soup.find('dd',attrs={'tit':'主要主题'}).findAll('ul')
        for i in primary_topic:
            tag1 = i.findAll('li')
            for j in tag1:
                primary_word.append(j.find('input')['value'])
        #次要主题
        secondary_topic = soup.find('dd',attrs={'tit':'次要主题'}).findAll('ul')
        for p in secondary_topic:
            tag2 = p.findAll('li')
            for q in tag2:
                secondary_word.append(q.find('input')['value'])
        # res_word = {'主要主题':primary_word,
        #             '次要主题':secondary_word}
        item = CnkiNewSpiderItem()
        item['key_word'] = response.meta['key_word']
        item['primary_topic'] = pymysql.escape_string(json.dumps(primary_word))
        item['secondary_topic'] = pymysql.escape_string(json.dumps(secondary_word))
        yield item
