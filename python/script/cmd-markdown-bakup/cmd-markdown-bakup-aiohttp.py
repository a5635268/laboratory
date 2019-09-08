import asyncio
import aiohttp
from markdown_base import *
from aiohttp import web
import collections

# 设定对多开几个协程
MAX_WORKERS = 1000

class DownError(Exception):
    def __init__(self, url, msg):
        self.url = url
        self.msg = msg


async def get_image(img_url):
    async with aiohttp.ClientSession() as client:
        async with client.get(img_url) as resp:
            if resp.status == 200:
                image = await resp.read()
                return image
            if resp.status == 404:
                raise Exception('404 not find')
            raise aiohttp.HttpProcessionError(
                code=resp.status, message=resp.reason,
                headers=resp.headers
            )


# 每个协程执行
async def download_one(img_url,semaphore):
    try:
        async with semaphore:
            image =await get_image(img_url)
    except Exception as exc:
        raise DownError(img_url,str(exc)) from exc
    else:
        file_path =  SAVE_PATH + str(img_url).split("/")[-1]
        if os.path.exists(file_path):
            return img_url
        # 开始写文件，wb代表写二进制文件
        with open(file_path,"wb") as f:
            f.write(image)
    return img_url


# 主线程执行
async def downloader_coro(img_url_list):
    counter = 0

    # 创建一个 asyncio.Semaphore 实例，最多允许激活MAX_WORKERS个使用这个计数器的协程
    semaphore = asyncio.Semaphore(MAX_WORKERS)
    # 多次调用 download_one 协程，创建一个协程对象列表
    to_do = [download_one(img_url, semaphore) for img_url in img_url_list]
    # 获取一个迭代器，这个迭代器会在所有协程运行结束后返回各自的future
    to_do_iter = asyncio.as_completed(to_do)
    for future in to_do_iter:
        try:
            res = await future# 获取asyncio.Future对象的结果（也可以调用future.result）
        except DownError as exc:
            errored(exc.url,exc.msg)
        else:
            succeed(res)
        counter += 1
    return counter

# 事件循环器
def asyncloop(img_url_list):
    # 判断有没有改目录
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)

    # 1. 获取事件循环
    loop = asyncio.get_event_loop()

    # 2. 主线程执行下载
    coro = downloader_coro(img_url_list)

    # 执行事件循环，直到wait_coro 运行结束；事件循环运行的过程中，这个脚本会在这里阻塞
    counts = loop.run_until_complete(coro)
    loop.close() # 关闭事件循环
    return counts

if __name__ == '__main__':
    main(asyncloop)