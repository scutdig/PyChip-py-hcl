from pyhcl import *
from pyhcl.simulator import Simulator


class ALU_Op:
    ALU_ADD = U(0)
    ALU_SUB = U(1)
    ALU_AND = U(2)
    ALU_OR = U(3)


class ALU(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        ctl=Input(U.w(2)),
        out=Output(U.w(32)),
    )

    io.out <<= LookUpTable(io.ctl, {
        ALU_Op.ALU_ADD: io.a + io.b,
        ALU_Op.ALU_SUB: io.a - io.b,
        ALU_Op.ALU_AND: io.a & io.b,
        ALU_Op.ALU_OR: io.a | io.b,
        ...: U(0)
    })


class ALU2(Module):
    io = IO(
        inst=Input(U.w(32)),
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        v=Input(Vec(4, U.w(32))),
        out=Output(U.w(32)),
    )

    sum = Sum(io.v)
    lut = LookUpTable(io.inst, {
        U.w(32)(10): VecInit([io.a * io.b, io.a / io.b, io.a ^ io.b, io.a % io.b]),
        U.w(32)(11): VecInit([io.a == io.b, io.a != io.b, io.a < io.b, io.a > io.b]),
        ...: VecInit([io.a + io.b, io.a - io.b, io.a & io.b, io.a | io.b])
    })

    io.out <<= Sum(lut) + sum


def main():
    s = Simulator(ALU())
    handler = s.handler

    # ---------- Simulation begin ---------- #
    s.start()

    for i in range(4):
        s.poke(handler.io.a, 200)
        s.poke(handler.io.b, 100)
        s.poke(handler.io.ctl, i)
        s.step()
        s.peek(handler.io.out)

    s.term()
    # ---------- Simulation end ---------- #


if __name__ == '__main__':
    main()
