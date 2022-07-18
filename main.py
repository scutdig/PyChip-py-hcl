from pyhcl import *

class FullAdder(Module):
    io = IO(
        a=Input(Bool),
        b=Input(Bool),
        cin=Input(Bool),
        sum=Output(Bool),
        cout=Output(Bool),
    )

    # Generate the sum
    io.sum @= io.a ^ io.b ^ io.cin

    # Generate the carry
    io.cout @= io.a & io.b | io.b & io.cin | io.a & io.cin

if __name__ == '__main__':
    # emit high firrtl
    Emitter.dump(Emitter.emit(FullAdder(), HighForm), "FullAdder.fir")
    # emit lowered firrtl
    Emitter.dump(Emitter.emit(FullAdder(), LowForm), "FullAdder.lo.fir")
    # emit verilog
    Emitter.dump(Emitter.emit(FullAdder(), Verilog), "FullAdder.v")
