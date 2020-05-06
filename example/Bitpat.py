from pyhcl import *


class Inst:
    ADD = BitPat("0000000??????????000?????0110011")
    SUB = BitPat("0100000??????????000?????0110011")
    AND = BitPat("0000000??????????111?????0110011")
    OR = BitPat("0000000??????????110?????0110011")
    LW = BitPat("?????????????????010?????0000011")
    SW = BitPat("?????????????????010?????0100011")


class Control:
    # ALUOP
    ALUOP_XXX = U(0)
    ALUOP_ADD = U(0)
    ALUOP_SUB = U(1)
    ALUOP_AND = U(2)
    ALUOP_OR = U(3)

    # MEM_READ
    MEM_READ_FALSE = U(0)
    MEM_READ_TRUE = U(1)

    # MEM_WRITE
    MEM_WRITE_FALSE = U(0)
    MEM_WRITE_TRUE = U(1)

    # REG_WRITE
    REG_WRITE_FALSE = U(0)
    REG_WRITE_TRUE = U(1)

    # map dict
    map = {
        Inst.ADD: VecInit([ALUOP_ADD, MEM_READ_FALSE, MEM_WRITE_FALSE, REG_WRITE_TRUE]),
        Inst.SUB: VecInit([ALUOP_SUB, MEM_READ_FALSE, MEM_WRITE_FALSE, REG_WRITE_TRUE]),
        Inst.AND: VecInit([ALUOP_AND, MEM_READ_FALSE, MEM_WRITE_FALSE, REG_WRITE_TRUE]),
        Inst.OR: VecInit([ALUOP_OR, MEM_READ_FALSE, MEM_WRITE_FALSE, REG_WRITE_TRUE]),
        Inst.LW: VecInit([ALUOP_XXX, MEM_READ_TRUE, MEM_WRITE_FALSE, REG_WRITE_TRUE]),
        Inst.SW: VecInit([ALUOP_XXX, MEM_READ_FALSE, MEM_WRITE_TRUE, REG_WRITE_FALSE]),
        ...: VecInit([ALUOP_XXX, MEM_READ_FALSE, MEM_WRITE_FALSE, REG_WRITE_FALSE])
    }


class BitPadTest(Module):
    io = IO(
        inst=Input(U.w(32)),
        ALUOP=Output(U.w(32)),
        MEM_READ=Output(U.w(32)),
        MEM_WRITE=Output(U.w(32)),
        REG_WRITE=Output(U.w(32)),

        a=Input(U.w(32)),
        b=Input(U.w(32)),
        v=Input(Vec(4, U.w(32))),
        out=Output(U.w(32)),
    )

    stmt_list = LookUpTable(io.inst, {
        Inst.ADD: VecInit([io.a * io.b, io.a / io.b, io.a ^ io.b, io.a % io.b]),
        Inst.SUB: VecInit([io.a == io.b, io.a != io.b, io.a < io.b, io.a > io.b]),
        ...: VecInit([io.a + io.b, io.a - io.b, io.a & io.b, io.a | io.b])
    })

    sum = Sum(io.v)

    io.out <<= Sum(stmt_list) + sum

    ctrl_signal = LookUpTable(io.inst, Control.map)

    v = VecInit([io.ALUOP, io.MEM_READ, io.MEM_WRITE, io.REG_WRITE])
    v <<= ctrl_signal


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(BitPadTest()), "bitpat.dir")
    Emitter.dumpVerilog(f)
