#!/usr/bin/env python
# coding=utf-8
from scrapy.selector import Selector
from scrapy.spiders import Rule,CrawlSpider
from scrapy.http import Request,FormRequest
from scrapy.linkextractors import LinkExtractor

from zhihu_spider.items import ZhihuSpiderItem

class ZhihuSpider(CrawlSpider):
    name = "zhihu_an_spider"
    allowed_domains = ["www.zhihu.com"]
    start_urls = [
        "http://www.zhihu.com"
    ]
    rules = (
        Rule(LinkExtractor(allow=(r'http://www\.zhihu\.com/question/\d+')),callback='parse',follow=True)
    ,)
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer": "http://www.zhihu.com/"
    }
    def start_request(self):
        return [Request("https://www.zhihu.com/login",meta={'cookie':1},callback = self.post_login)]

    def post_login(self,response):
        sel = Selector(response)
        print 'preparing login'
        xsrf = sel.xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print xsrf
        captcha_url = 'http://www.zhihu.com/captcha.gif'
        captcha = response.get(captcha_url,stream=True,headers=self.headers)
        with open('capcha.gif','wb') as f:
            for line in captcha.iter_content(10):
                f.write(line)
            f.close()
        print "输入验证码"+'\n'
        captcha_str = input()
        return [FormRequest.form_reponse(response,meta = {'cookiejar':response.meta['cookiejar']},
                                         headers = self.headers,
                                         formdata = {
                                             '_xsrf':xsrf,
                                             'email':'',
                                             'captcha':captcha_str,
                                             'remember_me':'true',
                                             'password':''
                                         },
                                        callback = self.after_login,
                                        dont_filter = True)]

    def after_login(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse_page(self,response):
        sel = Selector(response)
        item = ZhihuSpiderItem()

        urls = response.url
        names = sel.xpath('//span[@class="name"]/text()').extract()
        titles = sel.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        descriptions = sel.xpath('//div[@class="zm-editable-content"]/text()').extract()
        answers = sel.xpath('//div[@class="zm-editable-content clearfix"]/text()').extract()

        item['name'] = [n.encode('utf-8') for n in names]
        item['url'] = [n.encode('utf-8') for n in urls]
        item['title'] = [n.encode('utf-8') for n in titles]
        item['description'] = [n.encode('utf-8') for n in descriptions]
        item['answer'] = [n.encode('utf-8') for n in answers]
        yield item


