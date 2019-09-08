#! -*- coding: utf-8 -*-
# 单线程异步采集国旗

import asyncio
import aiohttp
from flags import save_flag, show, main, BASE_URL

async def get_flag(cc):
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    # 阻塞的操作通过协程实现，客户代码通过yield from 把指责委托给协程，以便异步操作
    # 注意：新版本的aiohttp必须要在每个协程中调用ClientSession.close()和_RequestContextManager._resp.release()，否则会报错
    # async with 自动调用__aexit__方法，而__aexit__方法包含了上面的关闭和释放方法
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as resp:
            assert resp.status == 200
            # 读取也是异步操作
            image = await resp.read()
            return image


async def download_one(cc):
    image =await get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    # 1. 获取事件循环
    loop = asyncio.get_event_loop()

    #2. 每个国旗下载都是一个协程，一次性激活获取各个国旗，构建一个生成器任务对象列表
    to_do = [download_one(cc) for cc in sorted(cc_list)]

    #3. 虽然函数名称是wait 但它不是阻塞型函数，wait 是一个协程，等传给他的所有协程运行完毕后结束
    wait_coro = asyncio.wait(to_do)

    # 4. 执行事件循环，直到wait_coro 运行结束；事件循环运行的过程中，这个脚本会在这里阻塞。
    res, _ = loop.run_until_complete(wait_coro)
    loop.close() # 关闭事件循环
    return len(res)

if __name__ == '__main__':
    main(download_many)