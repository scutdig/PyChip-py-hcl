from pyhcl import *


class AND(RawModule):
    io = IO(
        a=Input(U.w(1)),
        b=Input(U.w(1)),
        s=Output(U.w(1)),
    )

    myclock = Input(Clock())
    myreset = Input(Bool)
    io.s @= io.a ^ io.b
    _ = doAssert(myclock, io.a, io.s, "IF io.a is HIGH then io.s is HIGH")


if __name__ == '__main__':
    fa = AND()
    Emitter.dump(Emitter.emit(fa), "and.fir")