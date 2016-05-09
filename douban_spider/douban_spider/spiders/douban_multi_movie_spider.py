#!/usr/bin/env python
# coding=utf-8
from scrapy.selector import Selector
from scrapy.http import Request 
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor

from douban_spider.items import DoubanSpiderItem
class DoubanSpider(CrawlSpider):

    name = "douban_multi_movie_spider"
    allowed_domains = []
    
    start_urls = [
        'http://movie.douban.com/top250?start=0&filter=&type='
    ]

    rules=(
        Rule(LinkExtractor(allow=(r'http://movie\.douban\.com/top250\?start=\d+&filter=&type=')),callback='parse',follow=True)
        ,
    )

    def parse(self,response):
        print response

        sel = Selector(response)
        item = DoubanSpiderItem()

        movie_name = sel.xpath('//span[@class="title"][1]/text()').extract()
        star = sel.xpath('//div[@class="star"]/span[@class="rating_num"]/text()').extract()
        quote = sel.xpath('//p[@class="quote"]/span[@class="inq"]/text()').extract()

        item['movie_name'] = [n.encode('utf-8') for n in movie_name]
        item['star'] = [n.encode('utf-8') for n in star]
        item['quote'] = [n.encode('utf-8') for n in quote]

        yield item
        print item
        next_page = sel.xpath('//span[@class="next"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield Request(url,self.parse)
