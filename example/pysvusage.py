import random

from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import Simlite, DpiConfig
import random

class Add(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        out=Output(U.w(32))
    )


@sv(a=DataType.UInt, return_type=Reference(x=DataType.UInt))
def fn(a):
    return a + 10000


addpysvmodule(Add, fn)

class Rand(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        in2=Input(U.w(32)),
        out=Output(U.w(32))
    )


@sv(a=DataType.UInt, b=DataType.UInt, return_type=Reference(x=DataType.UInt))
def fn2(a, b):
    return random.randint(a, b)


addpysvmodule(Rand, fn2)
compile_and_binding_all()


class Top(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        c=Output(U.w(32))
    )

    wire = Wire(U.w(32))

    r = Rand()
    add = Add()
    r.io.in1 <<= io.a
    r.io.in2 <<= io.b
    wire <<= r.io.out
    add.io.in1 <<= wire
    io.c <<= add.io.out



if __name__ == '__main__':
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))

    s = Simlite(Top(), harness_code=None, dpiconfig=cfg)
    s.step([20, 20])
    s.step([15, 100])
    s.step([1000, 2000])
    s.step([999, 2010])
