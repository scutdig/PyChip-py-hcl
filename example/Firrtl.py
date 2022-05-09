from pyhcl import *

class Add(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        in2=Input(U.w(32)),
        out=Output(U.w(32)),
    )

class M(Module):
    io = IO(
        i=Input(U.w(32)),
        o=Output(U.w(32)),
    )

    bbox = Add()
    bbox.io.in1 <<= io.i
    bbox.io.in2 <<= io.i
    io.o <<= bbox.io.out

fircode = """module Add :
    input in1 : UInt<32>
    input in2 : UInt<32>
    output out : UInt<32>
    out <= add(in1, in2)
"""
addfirrtlmodule(Add, fircode)

if __name__ == '__main__':
    #Emitter.dumpVerilog(Emitter.dump(Emitter.emit(M()), "Top.fir"))
    from pyhcl.simulator import Simlite
    s = Simlite(M(), dpiconfig=None)