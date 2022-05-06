import asyncio
import time


async def a():
    print('Suspending a')
    await asyncio.sleep(3)
    print('Resuming a')


async def b():
    print('Suspending b')
    await asyncio.sleep(1)
    print('Resuming b')


def show_perf(func):
    print('*'*20)
    start = time.perf_counter()
    asyncio.run(func())
    print(f'{func.__name__} Cost: {time.perf_counter() - start}')


# 串行的执行
async def s1():
    await a()
    await b()


async def c1():
    await asyncio.gather(a(),b())


async def c2():
    await asyncio.wait([a(), b()])


# asyncio.create_task相当于把协程封装成Task
async def c3():
    task1 = asyncio.create_task(a())
    task2 = asyncio.create_task(b())
    print("XXX")
    await task2
    print("YYY")
    # await task2
    # await asyncio.sleep(3)
    print("ZZZ")

    # print("XXX")
    # await task2
    # print("YYY")
    # # await task1
    # print("ZZZ")


async def c4():
    task = asyncio.create_task(b())
    print("XXX")
    await a()
    print("YYY")
    # await task
    print("ZZZ")

    # print("XXX")
    # await task
    # print("YYY")
    # await a()
    # print("ZZZ")


# 直接await task不会对并发有帮助
async def s2():
    await asyncio.create_task(a())
    await asyncio.create_task(b())


async def c5():
    task = asyncio.ensure_future(b())
    print("XXX")
    await a()
    print("YYY")
    # await task
    print("ZZZ")


async def c6():
    loop = asyncio.get_event_loop()
    task = loop.create_task(b())
    print("XXX")
    await a()
    print("YYY")
    await task
    print("ZZZ")


if __name__ == '__main__':
    show_perf(c3)
