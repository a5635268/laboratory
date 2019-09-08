# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field() # 进行url的md5加密
    front_image_url = scrapy.Field() # 文章下图片的url地址
    front_image_path = scrapy.Field() # 图片的存放路径
    praise_nums = scrapy.Field() # 点赞数
    fav_nums = scrapy.Field() # 搜藏数
    comment_nums = scrapy.Field()
    tag = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()

class JobbolePostItem(scrapy.Item):
    post_url = scrapy.Field()
    image_url = scrapy.Field()