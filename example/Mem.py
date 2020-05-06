from pyhcl import *


class MemDemo(Module):
    io = IO(
        i=Input(U.w(8)),
        o=Output(U.w(8)),
    )

    m = Mem(10, U.w(8))
    m[U(2)] <<= io.i
    io.o <<= m[U(2)]


def main():
    f = Emitter.dump(Emitter.emit(MemDemo()), "mem.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
