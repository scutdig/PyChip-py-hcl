from functools import reduce

from pyhcl import *


class Test(Module):
    io = IO(
        DIO_stop=Output(U.w(1)),
        Jotaro_stop=Output(U.w(1))
    )

    counter = RegInit(U.w(32)(0))
    DIO_stop_r = RegInit(U.w(1)(1))
    Jotaro_stop_r = RegInit(U.w(1)(0))

    counter <<= counter + U(1)

    with when(counter == U(10)):
        io.DIO_stop <<= U(0)
        DIO_stop_r <<= U(0)
    with otherwise():
        io.DIO_stop <<= DIO_stop_r

    with when(io.DIO_stop == U(0)):
        io.Jotaro_stop <<= U(1)
        Jotaro_stop_r <<= U(1)
    with otherwise():
        io.Jotaro_stop <<= Jotaro_stop_r


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Test()), "test.fir"))
