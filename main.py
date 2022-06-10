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

class Mul3(Module):
    """
    Four-by-four multiply using a look-up table.
    """
    io = IO(
        x=Input(U.w(2)),
        y=Input(U.w(2)),
        z=Input(U.w(2)),
        o=Output(U.w(6)),
    )

    # --------------------------------
    # Calculate io.z = io.x * io.y by
    # building filling out tbl
    # --------------------------------

    tbl = VecInit(VecInit(VecInit(U.w(6)(i * j * k) for k in range(4)) for i in range(4)) for j in range(4))
    io.o <<= tbl[io.x][io.y][io.z]

if __name__ == '__main__':
    # emit high firrtl
    # Emitter.dump(Emitter.emit(FullAdder(), HighForm), "FullAdder.fir")
    # emit lowered firrtl
    # Emitter.dump(Emitter.emit(FullAdder(), LowForm), "FullAdder.lo.fir")
    # emit verilog
    Emitter.dump(Emitter.emit(Mul3(), Verilog), "Mul3.v")
