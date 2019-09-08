# -*- coding: utf-8 -*-
import scrapy

class LoggertestSpider(scrapy.Spider):
    name = 'loggertest'
    allowed_domains = ['httpbin.org']
    start_urls = [
        # "http://httpbin.org/",              # HTTP 200 expected
        # "http://httpbin.org/status/404",    # Not found error
        # "http://httpbin.org/status/500",    # server issue
        # "http://httpbin.org:345/",          # non-responding host, timeout expected
        "http://httphttpbinbin.org/",       # DNS error expected
    ]

    # 重写配置
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'jobbole.middlewares.ProcessAllExceptionMiddleware.ProcessAllExceptionMiddleware': 543,
        },
        'DOWNLOAD_DELAY': 1,  # 延时最低为2s
        'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 2,
        'REDIRECT_ENABLED' : False,
        'RETRY_ENABLED' : False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4  # 限制对该网站的并发请求数
    }

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin,
                                     errback=self.errback_httpbin,
                                 dont_filter=True)


    def prn_obj(self,obj):
        print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

    def parse_httpbin(self, response):
        print('Got successful response from {}'.format(response.url))
        # self.logger.info('Got successful response from {}'.format(response.url))

    # 记录中间件在
    def errback_httpbin(self, failure):
        # log all failures
        # self.logger.error(repr(failure))

        print(failure.value)
        # exit()
        #
        # # 响应信息
        # response = failure.value.response
        #
        # # 请求信息
        # # response.request
        # print('错误信息打印')
        #
        # print(response.status)
        # print(response._url)
