# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class ZhihuSpiderPipeline(object):

    def __init__(self):
        self.file = codecs.open('zhihu_sp.json',mode='wb',encoding='utf-8')

    def process_item(self, item, spider):
        line = 'the list:'+'\n'
        for i in range(len(item['name'])):
            question_name = {'qusetion_name':item['name'][i]}
            question_url = {'question_url':item['url'][i]}
            question_title = {'question_title':item['title'][i]}
            question_description = {'question_description':item['description'][i]}
            question_answer = {'question_answer':item['answer'][i]}
            line = line+json.dumps(question_name,ensure_ascii=False)
            line = line+json.dumps(question_url,ensure_ascii=False)
            line = line+json.dumps(question_title,ensure_ascii=False)
            line = line+json.dumps(question_description,ensure_ascii=False)
            line = line+json.dumps(question_answer,ensure_ascii=False)
        self.file.write(line)

    def close_spider(self,spider):
        self.file.close()
