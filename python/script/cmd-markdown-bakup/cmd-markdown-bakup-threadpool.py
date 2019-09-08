from concurrent import futures
from markdown_base import *

# 设定ThreadPoolExecutor 类最多使用几个线程
MAX_WORKERS = 200

def download(images):
    if not len(images):
        return 0
    workers = min(MAX_WORKERS, len(images))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(save_image2, sorted(images))
    return len(list(res))

if __name__ == '__main__':
    main(download)