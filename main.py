from pyhcl import *

class MOD(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        e=Input(Bool),
        z=Output(U.w(32)),
    )

    x = RegInit(U.w(32)(0))
    y = RegInit(U.w(32)(0))

    with when(x >= y):
        x <<= x - y

    with when(io.e):
        x <<= io.a
        y <<= io.b

    io.z <<= x

class FullAdder(Module):
    io = IO(
        a=Input(U.w(1)),
        b=Input(U.w(1)),
        cin=Input(U.w(1)),
        s=Output(U.w(1)),
        cout=Output(U.w(1))
    )

    io.s <<= io.a ^ io.b ^ io.cin
    io.cout <<= (io.a & io.b) | (io.a & io.cin) | (io.b & io.cin)


class MemDemo(Module):
    io = IO(
        i=Input(U.w(16)),
        o=Output(U.w(16)),
    )

    m = Mem(10, U.w(16))
    m[U(2)] <<= io.i
    io.o <<= m[U(2)]

class MuxVec(Module):
    io = IO(
        i=Input(Bool),
        o=Output(Vec(4, Vec(8, U.w(32)))),
    )

    a = VecInit(VecInit(U.w(32)(i) for i in range(8)) for _ in range(4))
    b = VecInit(VecInit(U.w(32)(i) for i in range(7, -1, -1)) for _ in range(4))

    io.o <<= Mux(io.i, a, b)

class GCD(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        e=Input(Bool),
        z=Output(U.w(32)),
        v=Output(Bool),
    )

    x = Reg(U.w(32))
    y = Reg(U.w(32))

    with when(x > y):
        x <<= x - y
    with otherwise():
        y <<= y - x

    with when(io.e):
        x <<= io.a
        y <<= io.b

    io.z <<= x
    io.v <<= y == U(0)

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
    # TODO Vec下标访问不能转换为可综合Verilog代码
    io.o <<= tbl[io.x][io.y][io.z]

if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Mul3()), "Mul3.fir"), True)
    # Emitter.dump(Emitter.emit(Mul3(), True), "Mul3.v")
    # Emitter.dumpLowForm(Emitter.dump(Emitter.emit(Mul3()), "Mul3.fir"), True)
    




# def main():
#     f = Emitter.dump(Emitter.emit(MOD()), "mod.v")
#     Emitter.dumpVerilog(f)


# if __name__ == '__main__':
#     main()


