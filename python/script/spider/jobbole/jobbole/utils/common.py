import hashlib
import pymysql
from jobbole.settings import *

def get_md5(url):
    if isinstance(url,str):
        url = url.encode()
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# 打印对象属性
def pri_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


def mysql_db():
    # 链接数据库 获取操作游标
    config = {
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'user': MYSQL_USER,
        'passwd': MYSQL_PASSWD,
        'database' : 'spider',
        'charset':'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    conn = pymysql.connect(**config)
    return conn
