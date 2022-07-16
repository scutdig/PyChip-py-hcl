from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import Simlite, DpiConfig
from queue import Queue
import asyncio


class Add(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        in2=Input(U.w(32)),
        out=Output(U.w(32))
    )


@sv(a=DataType.UInt, b=DataType.UInt, return_type=Reference(x=DataType.UInt))
def fn(a, b):
    return a + b


addpysvmodule(Add, fn)      # 黑盒与函数     # 转换得到.sv/bbox/Add.sv，（SV里调用python函数）
compile_and_binding_all()   # 编译得到共享库 到.build文件夹下, 生成 SV binding文件 （.sv/pkg/pysv_pkg.sv）


class Top(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        c=Output(U.w(32))
    )

    add = Add()
    add.io.in1 <<= io.a
    add.io.in2 <<= io.b
    io.c <<= add.io.out


from random import randint


class driver:
    def __init__(self, name, s: Simlite, time_period):
        self.name = name
        self.req_mb = Queue()
        self.simlite = s
        self.time_period = time_period

    async def run(self):
        for i in range(3):
            input_data = [15 + i, 10 + i]
            self.simlite.step(input_data)
            print("%s drivered data %s" % (self.name, input_data))
            await asyncio.sleep(self.time_period)


class monitor:
    def __init__(self, name, s: Simlite, time_period):
        self.name = name
        self.input_mb = Queue()
        self.output_mb = Queue()
        self.simlite = s
        self.cnt = self.simlite.cnt
        self.time_period = time_period

    async def run(self):
        await asyncio.sleep(self.time_period/2)
        while True:
            if self.simlite.cnt == self.cnt + 1:
                self.cnt = self.simlite.cnt
                input_data = self.simlite.inputs_values
                output_data = self.simlite.results
                print("%s monitored input data %s" % (self.name, input_data))
                print("%s monitored output data %s" % (self.name, output_data))
                self.input_mb.put(input_data)
                self.output_mb.put(output_data)
            await asyncio.sleep(self.time_period)


class checker:
    def __init__(self, name, time_period):
        self.name = name
        self.error_count = 0
        self.cmp_count = 0
        self.in_mb = Queue()
        self.out_mb = Queue()
        self.time_period = time_period

    async def run(self):
        await self.do_compare()

    async def do_compare(self):
        while True:
            while self.out_mb.empty() or self.in_mb.empty():
                await asyncio.sleep(self.time_period)
            outputs = self.out_mb.get()
            inputs = self.in_mb.get()
            # print(inputs, outputs)
            result = sum(inputs)
            if result == outputs[0]:
                print("succeed:output data %d is equal with desired data %d" % (outputs[0], result))
            else:
                print("failed:output data %d is not equal with desired data %d" % (outputs[0], result))

            self.cmp_count = self.cmp_count + 1
            # await asyncio.sleep(self.time_period)


async def func(s, time_period):
    driver1 = driver("driver", s, time_period)
    monitor1 = monitor("monitor", s, time_period)
    checker1 = checker("checker", time_period)
    monitor1.input_mb = checker1.in_mb
    monitor1.output_mb = checker1.out_mb
    driver_task = asyncio.create_task(driver1.run())
    monitor_task = asyncio.create_task(monitor1.run())
    checker_task = asyncio.create_task(checker1.run())

    await driver_task
    # await monitor_task
    await asyncio.sleep(1)


def main():
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), dpiconfig=cfg, debug=True)
    s.start()
    time_period = 0.1
    asyncio.run(func(s, time_period))

    s.close()


if __name__ == '__main__':
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), dpiconfig=cfg, debug=True)
    s.start()
    s.step([20, 20])
    s.step([15, 10])
    s.step([1000, 1])
    s.step([999, 201])
    s.close()
