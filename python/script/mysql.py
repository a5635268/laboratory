#安装PyMySQL：pip3 install PyMySQL
#!/usr/bin/python3
#coding=utf-8
#数据库操作类

import pymysql
import hashlib
import time

class SingletonModel:

    #数据库连接对象
    __db = None

    #游标对象
    __cursor = None

    def __new__(self, *args, **kwargs):
        if not hasattr(self, '_instance'):
            self._instance = super().__new__(self)
            # 批量定义
            if 'config' in kwargs:
                kwargs = kwargs['config']
            #主机
            host = 'host' in kwargs and kwargs['host'] or 'localhost'
            #端口
            port = 'port' in kwargs and kwargs['port'] or '3306'
            #用户名
            user = 'user' in kwargs and kwargs['user'] or 'root'
            #密码
            passwd = 'passwd' in kwargs and kwargs['passwd'] or '123456'
            #数据库
            db = 'database' in kwargs and kwargs['database'] or 'mypython'
            #编码
            charset = 'charset' in kwargs and kwargs['charset'] or 'utf8'
            # 打开数据库连接
            print('连接数据库...')
            self.__db = pymysql.connect(host=host,port=int(port),user=user,passwd=passwd,db=db,charset=charset)
            #创建一个游标对象 cursor
            #self.__cursor = self.__db.cursor()
            self.__cursor = self.__db.cursor(cursor=pymysql.cursors.DictCursor)
        return self._instance

    #返回执行execute()方法后影响的行数
    def execute(self,sql):
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
            #获取自增id
            rowcount = self.__cursor.rowcount
        except Exception as e:
            # 发生错误时回滚
            self.__db.rollback()
            print(e)
            return None
        return rowcount

        #返回执行execute()方法后影响的行数
    def query(self,sql,fields):
        try:
            # 执行SQL语句
            self.__cursor.execute(sql,fields)
            # 使用 fetchone() 方法获取单条数据.
            data = self.__cursor.fetchall()
        except Exception as e:
            self.__db.rollback()
            print(e)
            return None
        return data

    #增->返回新增ID
    def insert(self,**kwargs):
        table = kwargs['table']
        del kwargs['table']
        sql = 'insert into %s set '%table
        for k,v in kwargs.items():
            sql += "`%s`='%s',"%(k,v)
        sql = sql.rstrip(',')
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
            #获取自增id
            res = self.__cursor.lastrowid
        except:
            # 发生错误时回滚
            self.__db.rollback()
        return res

    #删->返回影响的行数
    def delete(self,**kwargs):
        table = kwargs['table']
        where = kwargs['where']
        sql = 'DELETE FROM %s where %s'%(table,where)
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
            #影响的行数
            rowcount = self.__cursor.rowcount
        except:
            # 发生错误时回滚
            self.__db.rollback()
        return rowcount

    #改->返回影响的行数
    def update(self,**kwargs):
        table = kwargs['table']
        #del kwargs['table']
        kwargs.pop('table')

        where = kwargs['where']
        kwargs.pop('where')

        sql = 'update %s set '%table
        for k,v in kwargs.items():
            sql += "`%s`='%s',"%(k,v)
        sql = sql.rstrip(',')
        sql += ' where %s'%where
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
            #影响的行数
            rowcount = self.__cursor.rowcount
        except:
            # 发生错误时回滚
            self.__db.rollback()
        return rowcount

    #查->单条数据
    def fetchone(self,**kwargs):
        table = kwargs['table']
        #字段
        field = 'field' in kwargs and kwargs['field'] or '*'
        #where
        where = 'where' in kwargs and 'where '+kwargs['where'] or ''
        #order
        order = 'order' in kwargs and 'order by '+ kwargs['order'] or ''

        sql = 'select %s from %s %s %s limit 1'%(field,table,where,order)
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.__cursor.fetchone()
        except:
            # 发生错误时回滚
            self.__db.rollback()
        return data

    #查->多条数据
    def fetchall(self,**kwargs):
        table = kwargs['table']
        #字段
        field = 'field' in kwargs and kwargs['field'] or '*'
        #where
        where = 'where' in kwargs and 'where '+kwargs['where'] or ''
        #order
        order = 'order' in kwargs and 'order by '+ kwargs['order'] or ''
        #limit
        limit = 'limit' in kwargs and 'limit '+ kwargs['limit'] or ''
        sql = 'select %s from %s %s %s %s'%(field,table,where,order,limit)
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.__cursor.fetchall()
        except:
            # 发生错误时回滚
            self.__db.rollback()
        return data

        #析构函数，释放对象时使用
    def __del__(self):
        # 关闭数据库连接
        self.__db.close()
        print('关闭数据库连接...')


# if __name__ == '__main__':
#
#     # 链接数据库 获取操作游标 (host='localhost',port=3306,user='root',passwd='root',db='mypython',charset='utf8')
#     config = {
#         'host': "127.0.0.1",
#         'port': 3306,
#         'user': 'root',
#         'passwd': '123456',
#         'database' : 'spider',
#         'charset':'utf8mb4'
#     }
#     dbObject = SingletonModel(config=config)

    # 语句插入
    # sql = "INSERT INTO `spider`.`user`(`name`, `pwd`, `insert_time`) VALUES ('22', '22', 222)"
    # res = dbObject.execute(sql)

    # 写入数据,返回插入的id
    # print('\n写入数据:')
    # res = dbObject.insert(table='user',name='aaaa',pwd='123456',insert_time=1530587307)
    # print(res)

    # 查询数据-单条,如果有多条数据，只会取第一条
    # print('\n查询数据-单条:')
    # res = dbObject.fetchone(table='user',where="name = 'aaaa' or pwd = '22'")
    # print(res)

    # 修改数据,返回影响的条数
    # print('\n修改数据:')
    # res = dbObject.update(table='user',where="id < 5",name='dddd')
    # print(res)

    # 删除数据,返回影响的条数
    # print('\n删除数据:')
    # res = dbObject.delete(table='user',where="id < 3")
    # print(res)

    #查询数据-多条,返回list
    # print('\n查询数据 - 多条:')
    # res = dbObject.fetchall(table='user',order="id desc")
    # print(res,type(res))
    # if res:
    #     for value in res:
    #         print('name:%s,date:%s' % (value['name'],value['insert_time']))