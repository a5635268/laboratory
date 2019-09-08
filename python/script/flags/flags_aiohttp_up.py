#! -*- coding: utf-8 -*-
# 单线程异步采集国旗

import asyncio
import collections
from collections import namedtuple
from enum import Enum
import aiohttp
from aiohttp import web

from flags import save_flag, show, main, BASE_URL

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ =  1000


Result = namedtuple('Result', 'status data')
HTTPStatus = Enum('Status', 'ok not_found error')

# 自定义异常用于包装其他HTTP货网络异常，并获取country_code，以便报告错误
class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code

async def get_flag(cc):
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    # 阻塞的操作通过协程实现，客户代码通过yield from 把指责委托给协程，以便异步操作
    # 注意：新版本的aiohttp必须要在每个协程中调用ClientSession.close()和_RequestContextManager._resp.release()，否则会报错
    # async with 自动调用__aexit__方法，而__aexit__方法包含了上面的关闭和释放方法
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as resp:
            if resp.status == 200:
                image = await resp.read()
                return image
            if resp.status == 404:
                raise web.HttpNotFound()

            raise aiohttp.HttpProcessionError(
                code=resp.status, message=resp.reason,
                headers=resp.headers
            )



async def download_one(cc,semaphore):
    # semaphore 参数是 asyncio.Semaphore 类的实例
    # Semaphore 类是同步装置，用于限制并发请求
    try:
        # semaphore当成上下文管理器使用,完成后自动释放
        # 如果semaphore 计数器的值小于所允许的最大值，只有当前协程会阻塞，如果大于的话，当前进程都会堵塞
        async with semaphore:
            image =await get_flag(cc)
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'ok'
        show(cc)
    return Result(status, cc)


async def downloader_coro(cc_list):
    counter = collections.Counter()
    # 创建一个 asyncio.Semaphore 实例，最多允许激活MAX_CONCUR_REQ个使用这个计数器的协程
    semaphore = asyncio.Semaphore(MAX_CONCUR_REQ)
    # 多次调用 download_one 协程，创建一个协程对象列表
    to_do = [download_one(cc, semaphore) for cc in sorted(cc_list)]
    # 获取一个迭代器，这个迭代器会在所有协程运行结束后返回future
    to_do_iter = asyncio.as_completed(to_do)
    for future in to_do_iter:
        # 迭代允许结束的 future
        try:
            res = await future# 获取asyncio.Future对象的结果（也可以调用future.result）
        except FetchError as exc:
            # 抛出的异常都包装在FetchError对象里（因为其继承了顶级异常对象）
            country_code = exc.country_code
            try:
                # 尝试从原来的异常 （__cause__）中获取错误消息
                error_msg = exc.__cause__.args[0]
            except IndexError:
                # 如果在原来的异常中找不到错误消息，使用所连接异常的类名作为错误消息
                error_msg = exc.__cause__.__class__.__name__
            if error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status
        counter[status] += 1
    return counter

def download_many(cc_list):

    # 1. 获取事件循环
    loop = asyncio.get_event_loop()

    #2. 内部进行批量下载
    coro = downloader_coro(cc_list)

    # 4. 执行事件循环，直到wait_coro 运行结束；事件循环运行的过程中，这个脚本会在这里阻塞。
    counts = loop.run_until_complete(coro)
    loop.close() # 关闭事件循环
    return counts

if __name__ == '__main__':
    main(download_many)