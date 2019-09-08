# -*- coding: utf-8 -*-
import scrapy
from jobbole.items import JobboleArticleItem,JobbolePostItem
from scrapy.http import Request
from jobbole.utils.common import get_md5
from urllib import parse
from datetime import datetime
import re

class JobbolepythonspiderSpider(scrapy.Spider):
    name = 'jobbolePythonSpider'

    # 所有的Request请求的链接都要基于此链接，否则就要加dontFilter=true
    allowed_domains = ['python.jobbole.com']

    # 父类的start_requests方法会请求start_urls里面的链接
    start_urls = ['http://python.jobbole.com/all-posts/']

    # 递归获取文章链接
    def parse(self, response):

        # # 列表文章节点,该节点包含了文章详情地址和图片链接
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            # 这里通过meta参数将图片的url传递进来，这里用parse.urljoin的好处是如果有域名我前面的response.url不生效
            # parse.urljoin封装自：urlparse.urljoin
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":parse.urljoin(response.url,image_url)},callback=self.parse_detail,errback=self.errback)


        # # 提取下一页并交给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url,callback=self.parse)

    # 记录中间件在
    def errback(self, failure):
        # log all failures
        # self.logger.error(repr(failure))
        print(failure)


    # 获取文章的详细内容
    def parse_detail(self,response):
        article_item = JobboleArticleItem()

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        article_item["title"] = title

        # 标签
        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tag =",".join(tag_list)
        article_item["tag"] = tag

        # 栏目名称
        category = tag_list[0]
        article_item["category"] = category

        front_image_url = response.meta.get("front_image_url","")  #文章封面图地址

        # 这个地方必须要list，便于管道循环下载
        article_item["front_image_url"] = [front_image_url]

        # 点赞数
        praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()
        praise_nums = 0 if len(praise_nums) == 0 else int(praise_nums[0])
        article_item["praise_nums"] = int(praise_nums)

        # 收藏数
        fav_nums  = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        match_re = re.match(".*(\d+).*",fav_nums)
        fav_nums = int(match_re.group(1)) if match_re else 0
        article_item["fav_nums"] = fav_nums

        # 评论数
        comment_nums =response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_com = re.match(".*(\d+).*",comment_nums)
        comment_nums = int(match_com.group(1)) if match_com else 0
        article_item["comment_nums"] = comment_nums

        # 内容
        # content = response.xpath('//div[@class="entry"]').extract()[0]
        article_item['content'] = ''

        #这里对地址进行了md5变成定长
        article_item["url_object_id"] = get_md5(response.url)
        article_item["url"] = response.url

        try:
            create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().split()[0]
            create_date = datetime.strptime(create_date,'%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.now().date()
        article_item["create_date"] = create_date


        yield article_item