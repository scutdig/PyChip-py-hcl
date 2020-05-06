from functools import reduce
from typing import List

from pyhcl import *


def myManyDynamicElementVecFir(length: int, consts: List):
    class MyManyDynamicElementVecFir(Module):
        io = IO(
            i=Input(U.w(8)),
            valid=Input(Bool),
            o=Output(U.w(8)),
        )

        taps = [io.i] + [RegInit(U.w(8)(0)) for _ in range(length)]
        for a, b in zip(taps, taps[1:]):
            with when(io.valid):
                b <<= a

        m = map(lambda x: x[0] * x[1], zip(taps, consts))
        io.o <<= reduce(lambda x, y: x + y, m)

    return MyManyDynamicElementVecFir()


def main():
    consts = []
    for i in range(4):
        consts.append(U(i))
    f = Emitter.dump(Emitter.emit(myManyDynamicElementVecFir(4, consts)), "filter.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
