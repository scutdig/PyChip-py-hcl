from pyhcl import *


class Mul1(Module):
    """
    Four-by-four multiply using a look-up table.
    """
    io = IO(
        x=Input(U.w(4)),
        y=Input(U.w(4)),
        z=Output(U.w(8)),
    )

    # --------------------------------
    # Calculate io.z = io.x * io.y by
    # building filling out muls
    # --------------------------------

    muls = [U.w(8)(i * j) for i in range(16) for j in range(16)]
    tbl = VecInit(muls)
    io.z <<= tbl[io.x << U(4) | io.y]


class Mul2(Module):
    """
    Four-by-four multiply using a look-up table.
    """
    io = IO(
        x=Input(U.w(4)),
        y=Input(U.w(4)),
        z=Output(U.w(8)),
    )

    # --------------------------------
    # Calculate io.z = io.x * io.y by
    # building filling out tbl
    # --------------------------------

    tbl = VecInit(VecInit(U.w(8)(i * j) for i in range(16)) for j in range(16))
    io.z <<= tbl[io.x][io.y]


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


def main():
    f = Emitter.dump(Emitter.emit(Mul1()), "mul.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
