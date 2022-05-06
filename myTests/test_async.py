# Eventloop 是asyncio应用的核心,把一些异步函数注册到这个事件循环上，事件循环会循环执行这些函数,
# 当执行到某个函数时，如果它正在等待I/O返回，如它正在进行网络请求，或者sleep操作，事件循环会暂停它的执行去执行其他的函数；
# 当某个函数完成I/O后会恢复，下次循环到它的时候继续执行。
# 因此，这些异步函数可以协同(Cooperative)运行：这就是事件循环的目标。

# await只能用在协程函数中, 所以想要用await关键字就还需要定义一个协程函数, 但最终的执行还是需要放到一个事件循环中进行
import asyncio
import time


async def testa(x):
    print("in myTests a")
    await asyncio.sleep(3)
    print("Resuming a")
    return x


async def testb(x):
    print("in myTests b")
    await asyncio.sleep(1)
    print('Resuming b')
    return x


# 先执行了testa函数，然后再执行了testb函数，是串行的依次执行的
async def main_1():
    start = time.time()
    resulta = await testa(1)
    resultb = await testb(2)
    print("myTests a result is %d" % resulta)
    print("myTests b result is %d" % resultb)
    print("use %s time" % (time.time()-start))


# testa和testb是同步在运行,最后将每个协程函数的结果返回，
# 注意，这里是gather()函数里的每一个协程函数都执行完了，它才结果，结果是一个列表，列表里的值顺序和放到gather函数里的协程的顺序是一致的
async def main_2():
    start = time.time()
    resulta, resultb = await asyncio.gather(testa(1), testb(2))
    print("myTests a result is %d" % resulta)
    print("myTests b result is %d" % resultb)
    print("use %s time" % (time.time() - start))


# 使用Task任务对象
# 使用asyncio.ensure_future(testa(1)) 返回一个task对象，此时task进入pending状态，并没有执行
# taska.done()返回False,表示它还没有结束
# 当调用await taska 时表示开始执行该协程，当执行结束以后，taska.done() 返回True
# 这时可以调用taska.result() 得到函数的返回值，如果协程还没有结束就调用result()方法则会抛异常
async def main_3():
    start = time.time()

    taska = asyncio.ensure_future(testa(1))
    taskb = asyncio.ensure_future(testb(2))

    print(taska)
    print(taskb)
    print(taska.done(), taskb.done())
    await taskb
    await taska
    print(taska.done(), taskb.done())

    print(taskb.result())
    print(taska.result())
    print("use %s time" % (time.time() - start))


# 创建task对象除了使用asyncio.ensure_future()方法还可以使用loop.create_task() 方法
async def main_4():
    start = time.time()

    taska = loop.create_task(testa(1))
    taskb = loop.create_task(testb(2))

    print(taska)
    print(taskb)
    print(taska.done(), taskb.done())
    await taskb
    await taska
    print(taska.done(), taskb.done())

    print(taskb.result())
    print(taska.result())
    print("use %s time" % (time.time() - start))


# asyncio.wait() 返回一个tuple对象
async def main_5():
    start = time.time()
    done, pending = await asyncio.wait([testa(1), testb(2)])
    print(list(done))
    print(list(pending))
    print(list(done)[0].result())
    print("use %s time" % (time.time() - start))


# gather是需要所有任务都执行结束，如果某一个协程函数崩溃了，则会抛异常，都不会有结果。
# wait可以定义函数返回的时机，可以是FIRST_COMPLETED(第一个结束的), FIRST_EXCEPTION(第一个出现异常的), ALL_COMPLETED(全部执行完，默认的)
async def main_6():
    start = time.time()
    done, pending = await asyncio.wait([testa(1), testb(2)], return_when=asyncio.tasks.FIRST_EXCEPTION)
    print(list(done))
    print(list(pending))
    print(list(done)[1].result())
    print("use %s time" % (time.time() - start))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_1())
    # loop.run_until_complete(main_2())
    # loop.run_until_complete(main_3())
    # loop.run_until_complete(main_4())
    # loop.run_until_complete(main_5())
    # loop.run_until_complete(main_6())
    loop.close()

