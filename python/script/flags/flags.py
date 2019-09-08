#! -*- coding: utf-8 -*-
# 单线程同步采集国旗

import os
import time
import sys
import requests

POP20_CC = ['CN', 'IN', 'US', 'ID', 'BR', 'PK', 'NG', 'BD', 'RU', 'JP', 'MX', 'PH', 'VN', 'ET', 'EG', 'DE', 'IR', 'TR', 'CD', 'FR']
BASE_URL = 'http://flupy.org/data/flags'  # <3>

DEST_DIR = "D:/_gang/python/python_basics/images/"  # <4>

# 保存图片
def save_flag(img, filename):  # <5>
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

# 下载图片
def get_flag(cc):  # <6>
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


# 显示一个字符串，然后刷新sys.stdout,目的是在一行消息中看到进度
def show(text):  # <7>
    print(text, end=' ')
    sys.stdout.flush()


def download_many(cc_list):  # <8>
    for cc in sorted(cc_list):  # <9>
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)


def main(download_many):  # <10>
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)  # <11> BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN