from pysv import sv, DataType, Reference
from pyhcl import *


class BBox(BlackBox):
    io = IO(
        in1=Input(U.w(64)),
        in2=Input(U.w(64)),
        out1=Output(U.w(64)),
        out2=Output(U.w(64)),
    )


@sv(a=DataType.ULongInt, b=DataType.ULongInt, return_type=Reference(x=DataType.ULongInt, y=DataType.ULongInt))
def f(a, b):
    return a+b, a-b


addpysvmodule(BBox, f)
compile_and_binding_all()


class M(Module):
    io = IO(
        i = Input(U.w(64)),
        o = Output(U.w(64)),
    )

    bbox = BBox()
    bbox.io.in1 <<= io.i
    bbox.io.in2 <<= io.i
    io.o <<= bbox.io.out1 ^ bbox.io.out2


if __name__ == '__main__':
    Emitter.dump(Emitter.emit(M()), "bbox.fir")