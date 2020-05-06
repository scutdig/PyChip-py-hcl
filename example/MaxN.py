from functools import reduce

from pyhcl import *


def maxN(n: int, w: int):
    def _max2(x: U, y: U):
        return Mux(x > y, x, y)

    class MaxN(Module):
        io = IO(
            ins=Input(Vec(n, U.w(w))),
            out=Output(U.w(w)),
        )

        io.out <<= reduce(_max2, io.ins)

        # temp = io.ins[0]
        # for x in io.ins[1:]:
        #     temp = Mux(temp > x, temp, x)
        # io.out <<= temp

    return MaxN()


def main():
    f = Emitter.dump(Emitter.emit(maxN(16, 32)), "maxN.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
