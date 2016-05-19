#!/usr/bin/env python
# coding=utf-8
import scrapy, json
from PIL import Image
from StringIO import StringIO
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request

class ZhihuSpider(scrapy.spiders.Spider):

    name = "test"

    def start_requests(self):
        return [FormRequest("http://www.zhihu.com/login/email", callback=self.init)]

    def init(self,response):
        self._xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        return Request('http://www.zhihu.com/captcha.gif?type=login', callback=self.login)

    def getcapid(self,response):
        Image.open(StringIO(response.body)).show()
        with open('captcha.gif', 'wb') as fp:
            fp.write(response.body)
        return raw_input('输入验证码: ')

    def login(self,response):
        return FormRequest("http://www.zhihu.com/login/email",formdata={
            'email': '',
            'password': '',
            'remember_me':'true',
            '_xsrf': self._xsrf,
            'captcha': self.getcapid(response),
        },callback=self.after_login)

    def after_login(self,response):
        if json.loads(response.body)['msg'].encode('utf8') == "登陆成功":
            yield self.make_requests_from_url('http://www.zhihu.com/people/timeship')
        else:
            print "验证码错误"

    def parse(self,response):
        print response.body
