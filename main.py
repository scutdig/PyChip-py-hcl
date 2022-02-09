from pyhcl import *


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


def main():
    f = Emitter.dump(Emitter.emit(MOD()), "mod.v")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()


