from pyhcl import *
from enum import Enum


Empty = U.w(2)(0)
Full = U.w(2)(1)
Nil = U.w(2)(2)


def BubbleFifoFactory(depth, size):
    class FifoRegister(Module):
        io = IO(
            write=Input(Bool),
            full=Output(Bool),
            din=Input(U.w(size)),

            read=Input(Bool),
            empty=Output(Bool),
            dout=Output(U.w(size))
        )

        stateReg = RegInit(U.w(2)(0))  # empty
        dataReg = RegInit(U.w(size)(0))

        with when(stateReg == Empty):
            with when(io.write):
                stateReg <<= Full
                dataReg <<= io.din
        with elsewhen(stateReg == Full):
            with when(io.read):
                stateReg <<= Empty
                dataReg <<= U.w(size)(0)

        io.full <<= (stateReg == Full)
        io.empty <<= (stateReg == Empty)
        io.dout <<= dataReg


    class BubbleFifo(Module):
        io = IO(
            write=Input(Bool),
            full=Output(Bool),
            din=Input(U.w(size)),

            read=Input(Bool),
            empty=Output(Bool),
            dout=Output(U.w(size))
        )

        FRs = [FifoRegister().io for i in range(depth)]
        for i in range(depth-1):
            FRs[i + 1].din <<= FRs[i].dout
            FRs[i + 1].write <<= ~FRs[i].empty
            FRs[i].read <<= ~FRs[i + 1].full

        io.din <<= FRs[0].din
        io.dout <<= FRs[0].dout
        io.full <<= FRs[0].full

        io.read <<= FRs[depth - 1].read
        io.empty <<= FRs[depth - 1].empty
        io.write <<= FRs[depth - 1].write

    return BubbleFifo()


