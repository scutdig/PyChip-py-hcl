from pyhcl import *


def matrixMul(x: int, y: int, z: int, width: int):
    class MatrixMul(Module):
        io = IO(
            a=Input(Vec(x, Vec(y, U.w(width)))),
            b=Input(Vec(y, Vec(z, U.w(width)))),
            o=Output(Vec(x, Vec(z, U.w(width)))),
            v=Output(Bool)
        )
        counter = RegInit(U.w(32)(0))

        res = Reg(Vec(x, Vec(z, U.w(width))))

        io.v <<= Bool(False)
        io.o <<= res
        with when(counter == U(x * z)):
            counter <<= U(0)
            io.v <<= Bool(True)
        with otherwise():
            counter <<= counter + U(1)
            row = counter / U(x)
            col = counter % U(x)
            res[row][col] <<= (lambda io, row, col: Sum(io.a[row][i] * io.b[i][col] for i in range(y)))(io, row, col)


        # # a trick of solving python3 closure scope problem
        # io.o <<= (lambda io: VecInit(VecInit(
        #     Sum(a * b for a, b in zip(a_row, b_col)) for b_col in zip(*io.b)) for a_row in io.a))(io)

    return MatrixMul()


def main():
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(matrixMul(2, 3, 2, 8)), "matrixMul.fir"))


if __name__ == '__main__':
    main()
