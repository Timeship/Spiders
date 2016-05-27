#!/usr/bin/env python
# coding=utf-8
import scrapy
import PIL
import StringIO

from zhihu_spider.items import ZhihuSpiderItem

class ZhihuSpider(scrapy.spiders.CrawlSpider):
    name = "zhihu_an_spider"
    allowed_domains = []
    start_urls = [
        "http://www.zhihu.com"
    ]
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer": "http://www.zhihu.com/"
    }
    def __init__(self,url=None):
        self.user_url = url

    def start_requests(self):
        yield scrapy.Request("http://www.zhihu.com/login/email",headers=self.headers,callback = self.init)

    def init(self,response):
        self._xrsf = scrapy.selector.Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        yield scrapy.Request('http://www.zhihu.com/captcha.gif?type=login',callback=self.post_login) 
    
    def getcapid(self,response):
        PIL.Image.open(StringIO.StringIO(response.body)).show()
        return raw_input('请输入验证码')

    def post_login(self,response):
        print 'preparing login'
        yield scrapy.FormRequest("http://www.zhihu.com/login/email",
                                         headers = self.headers,
                                         formdata = {
                                             '_xsrf':self._xrsf,
                                             'password':'',
                                             'captcha':self.getcapid(response),
                                             'remember_me':'true',
                                             'email':''
                                         },
                                        callback=self.request_zhihu)

    def request_zhihu(self,response):
        yield scrapy.Request(url=self.user_url+'/about',
                     headers = self.headers,
                     callback = self.user_parse,dont_filter=True) 
        yield scrapy.Request(url=self.user_url+'/followees',
                     headers = self.headers,
                     callback=self.user_start,dont_filter=True)
        yield scrapy.Request(url=self.user_url+'/followers',
                     headers = self.headers,
                     callback=self.user_start,dont_filter=True)
    
    def user_start(self,response):
        sel_root = response.xpath('//h2[@class="zm-list-content-title"]')
        if len(sel_root):
            for sel in sel_root:
                people_url = sel.xpath('a/@href').extract()[0]
                yield scrapy.Request(url=people_url+'/about',
                     headers=self.headers,
                     callback=self.user_parse,dont_filter=True)
                yield scrapy.Request(url=people_url+'/followees',
                     headers=self.headers,
                     callback=self.user_start,dont_filter=True)
                yield scrapy.Request(url=people_url+'/followers',
                     headers=self.headers,
                     callback=self.user_start,dont_filter=True)

    def user_parse(self, response):
        def value(list):
            return list[0] if len(list) else ''

        sel = response.xpath('//div[@class="zm-profile-header ProfileCard"]')

        item = ZhihuSpiderItem()
        item['url'] = response.url[:-6]
        item['name'] = sel.xpath('//a[@class="name"]/text()').extract()[0].encode('utf-8')
        item['bio'] = value(sel.xpath('//span[@class="bio"]/@title').extract()).encode('utf-8')
        item['location'] = value(sel.xpath('//span[contains(@class, "location")]/@title').extract()).encode('utf-8')
        item['business'] = value(sel.xpath('//span[contains(@class, "business")]/@title').extract()).encode('utf-8')
        item['gender'] = 0 if sel.xpath('//i[contains(@class, "icon-profile-female")]') else 1
        item['avatar'] = value(sel.xpath('//img[@class="Avatar Avatar--l"]/@src').extract())
        item['education'] = value(sel.xpath('//span[contains(@class, "education")]/@title').extract()).encode('utf-8')
        item['major'] = value(sel.xpath('//span[contains(@class, "education-extra")]/@title').extract()).encode('utf-8')
        item['employment'] = value(sel.xpath('//span[contains(@class, "employment")]/@title').extract()).encode('utf-8')
        item['position'] = value(sel.xpath('//span[contains(@class, "position")]/@title').extract()).encode('utf-8')
        item['content'] = value(sel.xpath('//span[@class="content"]/text()').extract()).strip().encode('utf-8')
        item['ask'] = int(sel.xpath('//div[contains(@class, "profile-navbar")]/a[2]/span[@class="num"]/text()').extract()[0])
        item['answer'] = int(sel.xpath('//div[contains(@class, "profile-navbar")]/a[3]/span[@class="num"]/text()').extract()[0])
        item['agree'] = int(sel.xpath('//span[@class="zm-profile-header-user-agree"]/strong/text()').extract()[0])
        item['thanks'] = int(sel.xpath('//span[@class="zm-profile-header-user-thanks"]/strong/text()').extract()[0])
        yield item
