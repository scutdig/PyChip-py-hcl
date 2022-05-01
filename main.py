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
    io.sum <<= io.a ^ io.b ^ io.cin

    # Generate the carry
    io.cout <<= io.a & io.b | io.b & io.cin | io.a & io.cin

if __name__ == '__main__':
    Emitter.dump(Emitter.emit(FullAdder(), Verilog), "FullAdder.v")


