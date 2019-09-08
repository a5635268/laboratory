#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
import logging
import time


# 日志格式

logging.basicConfig(filename='D://_gang//cmd-markdown//images//save_image.log',
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.ERROR)

# 列表表达式
def getImages(cmdPath):
    # 普通
    # md_list = [];
    # for dirpath,dirlist,filelist in os.walk(CMD_PATH):
    #     for filename in filelist:
    #         if os.path.splitext(filename)[1]=='.md':
    #             md_list.append(os.path.join(dirpath, filename))

    # 列表表达式
    mdList = [os.path.join(dirpath, filename) for dirpath,dirlist,filelist in os.walk(cmdPath) for filename in filelist if os.path.splitext(filename)[1]=='.md']
    reg = r'.*?(http(s?)://.+\.(jpg|gif|png|jpeg))'

    # 提前编译正则，并不区分大小写
    reg = re.compile(reg,re.I)

    images = []
    for filename in mdList:
        with open(filename, 'r', encoding='utf8') as f:
            str = f.read()
            imageList = re.findall(reg,str)
            for image in imageList:
                image and images.append(image[0])
    return images

def saveImg(images,savePath):
    if not isinstance(images,list):
        raise ValueError('invalid value type: images type must be list');
    if not os.path.exists(savePath):
        os.mkdir(savePath)

    for img in images:
        imgPath = savePath + img.split("/")[-1]
        if os.path.exists(imgPath):
            continue

        try:
            requestsObj = requests.get(img)

            # 错误码会直接抛出来
            requestsObj.raise_for_status()
        except Exception as e:
            logging.error(img + '保存失败：' + str(e))
            continue

        #开始写文件，wb代表写二进制文件
        with open(imgPath,"wb") as f:
            f.write(requestsObj.content)

start = time.time()
images = getImages('D://_gang//cmd-markdown');
saveImg(images,'D://_gang//cmd-markdown//images//');
speed = time.time() - start
msg = 'image downloaded in {:.2f}s'
print(msg.format(speed))