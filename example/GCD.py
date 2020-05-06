from pyhcl import *


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
    io.v <<= y == U(0)


def main():
    f = Emitter.dump(Emitter.emit(GCD()), "gcd.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
