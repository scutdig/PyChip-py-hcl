import random

from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import Simlite, DpiConfig
import random

class MOD(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        e=Input(Bool),
        z=Output(U.w(32)),
    )

    x = RegInit(U.w(32)(0))
    y = RegInit(U.w(32)(0))

    with when(x >= y):
        x <<= x - y

    with when(io.e):
        x <<= io.a
        y <<= io.b

    io.z <<= x

class FullAdder(Module):
    io = IO(
        a=Input(U.w(1)),
        b=Input(U.w(1)),
        cin=Input(U.w(1)),
        s=Output(U.w(1)),
        cout=Output(U.w(1))
    )

    io.s <<= io.a ^ io.b ^ io.cin
    io.cout <<= (io.a & io.b) | (io.a & io.cin) | (io.b & io.cin)


class MemDemo(Module):
    io = IO(
        i=Input(U.w(16)),
        o=Output(U.w(16)),
    )

    m = Mem(10, U.w(16))
    m[U(2)] <<= io.i
    io.o <<= m[U(2)]

class MuxVec(Module):
    io = IO(
        i=Input(Bool),
        o=Output(Vec(4, Vec(8, U.w(32)))),
    )

    a = VecInit(VecInit(U.w(32)(i) for i in range(8)) for _ in range(4))
    b = VecInit(VecInit(U.w(32)(i) for i in range(7, -1, -1)) for _ in range(4))

    io.o <<= Mux(io.i, a, b)

class GCD(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        e=Input(Bool),
        z=Output(U.w(32)),
        v=Output(Bool),
    )

    x = Reg(U.w(32))
    y = Reg(U.w(32))

    with when(x > y):
        x <<= x - y
    with otherwise():
        y <<= y - x

    with when(io.e):
        x <<= io.a
        y <<= io.b

    io.z <<= x
    io.v <<= y == U.w(32)(0)

class Mul3(Module):
    """
    Four-by-four multiply using a look-up table.
    """
    io = IO(
        x=Input(U.w(2)),
        y=Input(U.w(2)),
        z=Input(U.w(2)),
        o=Output(U.w(6)),
    )

    # --------------------------------
    # Calculate io.z = io.x * io.y by
    # building filling out tbl
    # --------------------------------

    tbl = VecInit(VecInit(VecInit(U.w(6)(i * j * k) for k in range(4)) for i in range(4)) for j in range(4))
    io.o <<= tbl[io.x][io.y][io.z]


class Add(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        out=Output(U.w(32))
    )


# @sv(a=DataType.UInt, return_type=Reference(x=DataType.UInt))
# def fn(a):
#     return a + 10000


# addpysvmodule(Add, fn)

class Rand(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        in2=Input(U.w(32)),
        out=Output(U.w(32))
    )


# @sv(a=DataType.UInt, b=DataType.UInt, return_type=Reference(x=DataType.UInt))
# def fn2(a, b):
#     return random.randint(a, b)


# addpysvmodule(Rand, fn2)
# compile_and_binding_all()


class Top(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        c=Output(U.w(32))
    )

    wir = Wire(U.w(32))

    r = Rand()
    add = Add()
    r.io.in1 <<= io.a
    r.io.in2 <<= io.b
    wir <<= r.io.out
    add.io.in1 <<= wir
    io.c <<= add.io.out



if __name__ == '__main__':
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(GCD()), "GCD.fir"), True)
    Emitter.dump(Emitter.emit(FullAdder(), LowForm), "FullAdder.lo.fir")
    # Emitter.dumpLoweredForm(Emitter.dump(Emitter.emit(Top()), "Top.fir"), True)
    # cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))

    # s = Simlite(Top(), harness_code=None, dpiconfig=cfg, debug=True)
    # s.start()
    # s.step([20, 20])
    # s.step([15, 100])
    # s.step([1000, 2000])
    # s.step([999, 2010])

# def main():
#     f = Emitter.dump(Emitter.emit(MOD()), "mod.v")
#     Emitter.dumpVerilog(f)


# if __name__ == '__main__':
#     main()


