from pyhcl import *


class MuxVec(Module):
    io = IO(
        i=Input(Bool),
        o=Output(Vec(4, Vec(8, U.w(32)))),
    )

    a = VecInit(VecInit(U.w(32)(i) for i in range(8)) for _ in range(4))
    b = VecInit(VecInit(U.w(32)(i) for i in range(7, -1, -1)) for _ in range(4))

    io.o <<= Mux(io.i, a, b)


def main():
    f = Emitter.dump(Emitter.emit(MuxVec()), "muxVec.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
