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

class ALU_Op:
    ALU_ADD = U(0)
    ALU_SUB = U(1)
    ALU_AND = U(2)
    ALU_OR = U(3)


class ALU(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        ctl=Input(U.w(2)),
        out=Output(U.w(32)),
    )

    io.out <<= LookUpTable(io.ctl, {
        ALU_Op.ALU_ADD: io.a + io.b,
        ALU_Op.ALU_SUB: io.a - io.b,
        ALU_Op.ALU_AND: io.a & io.b,
        ALU_Op.ALU_OR: io.a | io.b,
        ...: U(0)
    })

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

if __name__ == '__main__':
    Emitter.dump(Emitter.emit(ALU(), Verilog), "ALU.v")
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(ALU()), "ALU.fir"), True)


