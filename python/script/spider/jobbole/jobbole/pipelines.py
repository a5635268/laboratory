# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import json
import codecs
import pymysql
from twisted.enterprise import adbapi
from jobbole.utils.common import *

class JobbolePipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlTwistedPipline(object):
    '''
    采用异步的方式插入数据
    '''
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            port = settings["MYSQL_PORT"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWD"],
            db = settings["MYSQL_DB"],
            use_unicode = True,
            charset="utf8mb4",
        )
        dbpool = adbapi.ConnectionPool("pymysql",**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        '''
        使用twisted将mysql插入变成异步
        :param item:
        :param spider:
        :return:
        '''
        query = self.dbpool.runInteraction(self.do_insert,item)
        # 无效
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        #处理异步插入的异常
        # print('-----------------',end='\n')
        print(failure.value)
        print(item._values)
        # print('item')
        # pri_obj(item)
        #
        # print('spider')
        # pri_obj(spider)
        # print('-----------------',end='\n')

    def do_insert(self,cursor,item):
        #具体插入数据
        insert_sql = '''
        insert into jobbole_python_article(title,create_date,url,url_object_id,image_url,comment_nums,fav_nums,praise_nums,tag,category,content) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cursor.execute(insert_sql,(item["title"],item["create_date"],item["url"],item["url_object_id"],item["front_image_url"],item["comment_nums"],item["fav_nums"],item["praise_nums"],item["tag"],item["category"],item["content"]))



class ArticleImagePipeline(ImagesPipeline):
    '''
    对图片的处理
    '''
    def item_completed(self, results, item, info):

        # 想获取图片保存本地的地址
        for ok ,value in results:
            if ok:
                image_file_path = value["path"]
                item['front_image_path'] = image_file_path
            else:
                item['front_image_path'] = ""

        return item