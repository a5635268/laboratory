from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from jobbole.utils.common import *
from datetime import datetime
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message

class ProcessAllExceptionMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def __init__(self):
        self.mysql_db = mysql_db()

    def process_response(self,request,response,spider):
        if response.status != 200:
            reason = response_status_message(response.status)
            print('Got bad url: <%s> (%s) : %s' % (response.url,response.status,reason))
            self._insert_db(request.url,reason,response.status)

            # 这里抛出的错误可以抛到spider里面的
            raise IgnoreRequest(reason)

        #其他状态码不处理
        return response

    def process_exception(self,request,exception,spider):

        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            #在日志中打印异常类型
            msg = 'Got exception: %s' % (exception)

        # 打印出未捕获到的异常
        msg = 'not contained exception: %s' % exception
        print(msg)
        self._insert_db(request.url, msg)
        return None

    def _insert_db(self, url , msg, code=-1):
        sql = ''' INSERT INTO `test`(`url`, `status`, `reason`) VALUES (%s, %s, %s) '''
        cursor = self.mysql_db.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql,[url,code,msg])
            # 提交到数据库执行
            self.mysql_db.commit()
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.mysql_db.rollback()
            # 抛出错误到其他异常处理函数（一般是scrapy.Request.errback函数）
            raise IgnoreRequest(str(e))

        # 关闭数据库连接
        self.mysql_db.close()

    def _faillog(self, request, errorType, reason, spider):
         print("%(now)s [%(error)s] %(url)s reason: %(reason)s \r\n" %
               {'now':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'error': errorType,
                'url': request.url,
                'reason': reason})