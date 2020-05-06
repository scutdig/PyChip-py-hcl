from pyhcl import *


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


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(FullAdder()), "FullAdder.fir"))
