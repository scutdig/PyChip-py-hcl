from pyhcl import *


class BBox(BlackBox):
    io = IO(
        in1=Input(U.w(64)),
        in2=Input(U.w(64)),
        out=Output(U.w(64)),
    )


class M(Module):
    io = IO(
        i = Input(U.w(64)),
        o = Output(U.w(64)),
    )

    bbox = BBox()
    bbox.io.in1 <<= io.i
    bbox.io.in2 <<= io.i
    io.o <<= bbox.io.out


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(M()), "bbox.fir"))
