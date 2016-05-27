# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import json
#import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import mongoengine
mongoengine.connect('zhihudata',host='localhost:27017')

class ZhihuMongo(mongoengine.Document):
    url = mongoengine.StringField()
    name = mongoengine.StringField()
    bio = mongoengine.StringField()
    location = mongoengine.StringField()
    business = mongoengine.StringField()
    gender = mongoengine.StringField()
    avatar = mongoengine.StringField()
    education = mongoengine.StringField()
    major = mongoengine.StringField()
    employment = mongoengine.StringField()
    position = mongoengine.StringField()
    content = mongoengine.StringField()
    ask = mongoengine.StringField()
    answer = mongoengine.StringField()
    agree = mongoengine.StringField()
    thanks = mongoengine.StringField()
class ZhihuSpiderPipeline(object):
    def process_item(self,item,spider):
        new_profile = ZhihuMongo(
            url = item['url'],
            name = item['name'],
            bio = item['bio'],
            location = item['location'],
            business = item['business'],
            gender = str(item['gender']),
            avatar = item['avatar'],
            education = item['education'],
            major = item['major'],
            employment = item['employment'],
            position = item['position'],
            content = item['content'],
            ask = str(item['ask']),
            answer = str(item['answer']),
            agree = str(item['agree']),
            thanks = str(item['thanks'])
            )
        new_profile.save()
        return item
