from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import DpiConfig, Simulator

class Xor(BlackBox):
    io = IO(
        in1=Input(U.w(1)),
        in2=Input(U.w(1)),
        out=Output(U.w(1))
    )

@sv(a=DataType.Bit, b=DataType.Bit, return_type=Reference(x = DataType.Bit))
def fn(a, b):
    return a ^ b

addpysvmodule(Xor, fn)
compile_and_binding_all()


class Top(Module):
    io = IO(
        a=Input(U.w(1)),
        b=Input(U.w(1)),
        c=Output(U.w(1))
    )

    xor = Xor()
    xor.io.in1 <<= io.a
    xor.io.in2 <<= io.b
    io.c <<= xor.io.out


from random import randint

if __name__ == '__main__':
    cfg = DpiConfig()
    #Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))

    s = Simulator(Top(),cfg)
    
    handler = s.handler

    # ---------- Simulation begin ---------- #
    s.start()

    for i in range(16):
        s.poke(handler.io.a, randint()&1)
        s.poke(handler.io.b, randint()&1)
        s.step()
        s.peek(handler.io.c)
    s.term()
    # ---------- Simulation end ---------- #
    