from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import Simlite, DpiConfig


class Add(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        in2=Input(U.w(32)),
        out=Output(U.w(32))
    )


@sv(a=DataType.UInt, b=DataType.UInt, return_type=Reference(x=DataType.UInt))
def fn(a, b):
    return a + b


addpysvmodule(Add, fn)
compile_and_binding_all()


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


import time


def test():
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), dpiconfig=cfg, debug=True)
    time1 = time.time()
    inputs = [[2000, 230032]]*40
    for i in range(2):
        s.start_task(f"task_{i}", inputs)
    time2 = time.time()
    print("time = " + str(time2 - time1))
    s.start_task(f"task_3", inputs)
    time3 = time.time()
    print("time = " + str(time3 - time2))
    s.close()


if __name__ == '__main__':
    test()