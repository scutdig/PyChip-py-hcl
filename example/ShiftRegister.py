from pyhcl import *


class ShiftRegister(Module):
    io = IO(
        i=Input(Bool),
        o=Output(Bool),
        en=Input(Bool),
    )

    r0 = RegInit(U(0))
    r1 = RegInit(U(0))
    r2 = RegInit(U(0))
    r3 = RegInit(U(0))

    with when(io.en):
        r0 <<= io.i
        r1 <<= r0
        r2 <<= r1
        r3 <<= r2

    io.o <<= r3


def main():
    f = Emitter.dump(Emitter.emit(ShiftRegister()), "shiftR.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
