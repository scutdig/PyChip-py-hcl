# from pyhcl import *
# from pysv import sv, DataType, Reference
# from pyhcl.simulator import Simlite, DpiConfig
from queue import Queue
import asyncio
from injector.reader import read_wave


# class Add(BlackBox):
#     io = IO(
#         in1=Input(U.w(32)),
#         in2=Input(U.w(32)),
#         out=Output(U.w(32))
#     )
#
#
# @sv(a=DataType.UInt, b=DataType.UInt, return_type=Reference(x=DataType.UInt))
# def fn(a, b):
#     return a + b
#
#
# addpysvmodule(Add, fn)      # 黑盒与函数     # 转换得到.sv/bbox/Add.sv，（SV里调用python函数）
# compile_and_binding_all()   # 编译得到共享库 到.build文件夹下, 生成 SV binding文件 （.sv/pkg/pysv_pkg.sv）
#
#
# class Top(Module):
#     io = IO(
#         a=Input(U.w(32)),
#         b=Input(U.w(32)),
#         c=Output(U.w(32))
#     )
#
#     add = Add()
#     add.io.in1 @= io.a
#     add.io.in2 @= io.b
#     io.c @= add.io.out


from random import randint


class in_intf:
    def __init__(self):
        self.input_data = []


class out_intf:
    def __init__(self):
        self.output_data = []


# class driver:
#     def __init__(self, name, s: Simlite, time_period):
#         self.name = name
#         self.req_mb = Queue()
#         self.simlite = s
#         self.time_period = time_period
#
#     async def run(self):
#         for i in range(3):
#             input_data = [15 + i, 10 + i]
#             self.simlite.step(input_data)
#             print("%s drivered data %s" % (self.name, input_data))
#             await asyncio.sleep(self.time_period)
#
#     def set_interface(self, intf):
#         self.intf = intf


class in_monitor:
    def __init__(self, name, time_period):
        self.name = name
        self.input_mb = Queue()
        self.time_period = time_period
        self.input_data = 0

    async def run(self):
        await asyncio.sleep(self.time_period/2)
        while True:
            if self.intf.input_data != self.input_data:
                self.input_data = self.intf.input_data
                print("%s monitored input data %s" % (self.name, self.input_data))
                self.input_mb.put(self.input_data)
            await asyncio.sleep(self.time_period)

    def set_interface(self, intf):
        self.intf = intf


class out_monitor:
    def __init__(self, name, time_period):
        self.name = name
        self.output_mb = Queue()
        self.time_period = time_period
        self.output_data = 0

    async def run(self):
        await asyncio.sleep(self.time_period/2)
        while True:
            if self.intf.output_data != self.output_data:
                self.output_data = self.intf.output_data
                print("%s monitored output data %s" % (self.name, self.output_data))
                self.output_mb.put(self.output_data)
            await asyncio.sleep(self.time_period)

    def set_interface(self, intf):
        self.intf = intf


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


async def inject_values(time_period, in_intf, out_intf, wavefile):
    data = waveRead(wavefile)
    sim_time = 0
    while True:
        print()
        # values为字典{'信号':'值',...}--存放仿真时刻sim_time时各信号量的值
        values = data.get_values_at(sim_time)
        # print(values)

        # 注入当前仿真时刻的信号与值
        # injector.inject_values(values)
        input_data = [values['TOP.io_a'], values['TOP.io_b']]
        input_data = [int(k, base=2) for k in input_data]
        output_data = [values['TOP.io_c']]
        output_data = [int(k, base=2) for k in output_data]
        in_intf.input_data = input_data
        out_intf.output_data = output_data
        print("inject input_data %s and output_data %s" % (input_data, output_data))

        await asyncio.sleep(time_period)

        previous_time = sim_time
        # 得到仿真时刻sim_time后的一个变化时刻，若无则返回None
        sim_time = data.get_next_event(sim_time)

        if sim_time is None:
            break
        # await Timer(sim_time - previous_time)

    # for i in range(3):
    #     input_data = [15 + i, 10 + i]
    #     output_data = [sum(input_data)]
    #     in_intf.input_data = input_data
    #     out_intf.output_data = output_data
    #     print("inject input_data %s and output_data %s" % (input_data, output_data))
    #     await asyncio.sleep(time_period)
    pass


def waveRead(wavefile):
    replay_block = []
    excluded_sigs = []
    inputs_only = False
    data = read_wave(wavefile, replay_block, inputs_only, excluded_sigs)  # VcdReader对象
    print(data.signal_values)
    return data


async def func(time_period):
    # driver1 = driver("driver", s, time_period)
    i_monitor = in_monitor("in_monitor", time_period)
    o_monitor = out_monitor("out_monitor", time_period)
    checker1 = checker("checker", time_period)
    i_monitor.input_mb = checker1.in_mb
    o_monitor.output_mb = checker1.out_mb
    i_intf = in_intf()
    o_intf = out_intf()
    i_monitor.set_interface(i_intf)
    o_monitor.set_interface(o_intf)

    # driver_task = asyncio.create_task(driver1.run())

    i_monitor_task = asyncio.create_task(i_monitor.run())
    o_monitor_task = asyncio.create_task(o_monitor.run())
    checker_task = asyncio.create_task(checker1.run())

    # await driver_task
    # await monitor_task
    wavefile = "simulation/wave.vcd"
    inject_task = asyncio.create_task(inject_values(time_period, i_intf, o_intf, wavefile))
    await inject_task
    await asyncio.sleep(1)


def main():
    # cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    # s = Simlite(Top(), dpiconfig=cfg, debug=True)
    # s.start()
    time_period = 0.1
    asyncio.run(func(time_period))

    # s.close()


if __name__ == '__main__':
    # cfg = DpiConfig()
    # # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    # s = Simlite(Top(), dpiconfig=cfg, debug=True)
    # s.start()
    # s.step([20, 20])
    # s.step([15, 10])
    # s.step([1000, 1])
    # s.step([999, 201])
    # s.close()
    # wavefile = "../simulation/wave.vcd"
    # waveRead(wavefile)
    main()