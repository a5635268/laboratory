#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,sys
import re
import requests
import logging
import redis
from urllib.request import urlretrieve
import time

#redis
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)

# redisKey
ALL_IMAGES_SET_KEY = 'pythontest:images:all:set'
COMPLETED_IMAGES_SET_KEY = 'pythontest:images:completed:set'
WITHOUT_IMAGES_SET_KEY = 'pythontest:images:without:set'

# path
FILE_PATH = 'D:/_gang/cmd-markdown'
SAVE_PATH = 'D:/_gang/cmd-markdown/images/'
LOG_PATH = 'D:/_gang/cmd-markdown/images/log.log'

# 日志格式
logging.basicConfig(filename= LOG_PATH,
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.ERROR)


def get_redis():
    '''
    获取redis实例
    :return:
    '''
    # connection_pool = redis.ConnectionPool(host='127.0.0.1', db=1,port=6379,decode_responses=True)
    connection_pool = redis.ConnectionPool(host='172.28.3.24', db=1,port=6379,decode_responses=True)
    return redis.Redis(connection_pool=connection_pool)


def get_files(path,ext):
    '''
    在某路径下根据某扩展名获取文件列表
    只支持两层结构目录
    :param path:
    :param ext: example： .md .html .txt
    :return:
    '''
    files = [os.path.join(dirpath, filename) for dirpath,dirlist,filelist in os.walk(path) for filename in filelist if os.path.splitext(filename)[1] == ext]
    return files;


def get_images(files):
    '''
    获取图片
    :param files:
    :return:
    '''
    reg = r'.*?(http(s?)://.+\.(jpg|gif|png|jpeg))'

    # 提前编译正则，并不区分大小写
    reg = re.compile(reg,re.I)

    images = []
    for filename in files:
        with open(filename, 'r', encoding='utf8') as f:
            str = f.read()
            imageList = re.findall(reg,str)
            for image in imageList:
                image and images.append(image[0])
    return images


def get_download_images(images):
    '''
    真正要下载的图片（增量下载）
    :param images:
    :return:
    '''
    redis = get_redis()
    for img in images:
        # 存进集合里面，自动去重
        redis.sadd(ALL_IMAGES_SET_KEY,img)

    # 全部图片 - 已下载的图片 - 不需要下载的图片 = 要下载的图片
    download_images = redis.sdiff(ALL_IMAGES_SET_KEY,COMPLETED_IMAGES_SET_KEY,WITHOUT_IMAGES_SET_KEY)
    return download_images

def save_image(img):
    '''
    保存图片
    :param img:
    :param path:
    :return:
    '''
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    file_path =  SAVE_PATH + str(img).split("/")[-1]
    if os.path.exists(file_path):
        return True
    try:
        requests_obj = requests.get(img)

        # 错误码会直接抛出来
        requests_obj.raise_for_status()
    except Exception as e:
        return errored(img,str(e))

    # 开始写文件，wb代表写二进制文件
    with open(file_path,"wb") as f:
        f.write(requests_obj.content)

    return succeed(img)


def save_image2(img):
    '''
    通过urlretrieve来保存，减少了代码量
    :param img:
    :param path:
    :return:
    '''
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    img = str(img)
    file_path =  SAVE_PATH + img.split("/")[-1]
    if os.path.exists(file_path):
        return True
    try:
        urlretrieve(img, file_path)
    except Exception as e :
        return errored(img,str(e))
    succeed(img)

def succeed(img):
    redis = get_redis()
    redis.sadd(COMPLETED_IMAGES_SET_KEY,img);
    print('%s 保存成功' % img)
    sys.stdout.flush()

def errored(img,msg):
    redis = get_redis()
    redis.sadd(WITHOUT_IMAGES_SET_KEY,img)
    logging.error('[%s] 保存失败: %s' % (img,msg))
    print('[%s] 保存失败: %s' % (img,msg))
    sys.stdout.flush()

def main(download):
    start = time.time()
    files = get_files(FILE_PATH,'.md')
    images = get_images(files)
    download_images = get_download_images(images)
    count = download(download_images)
    speed = time.time() - start
    msg = '\n{} image downloaded in {:.2f}s'
    print(msg.format(count, speed))