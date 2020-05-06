from pyhcl import *

W = 8  # 位宽


def matrixMul(x: int, y: int, z: int):
    """
    x*y × y*z 矩阵乘法电路
    """

    class MatrixMul(Module):
        io = IO(
            a=Input(Vec(x, Vec(y, U.w(W)))),
            b=Input(Vec(y, Vec(z, U.w(W)))),
            o=Output(Vec(x, Vec(z, U.w(W)))),
        )

        for i, a_row in enumerate(io.a):
            for j, b_col in enumerate(zip(*io.b)):
                io.o[i][j] <<= Sum(a * b for a, b in zip(a_row, b_col))

    return MatrixMul()


def bias(n):
    return U.w(W)(n)


def weight(lst):
    return VecInit(U.w(W)(i) for i in lst)


def neurons(w, b):
    """
    参数：权重向量 w，偏移量 b
    输出：神经网络神经元电路  *注：暂无通过非线性传递函数
    """

    class Unit(Module):
        io = IO(
            i=Input(Vec(len(w), U.w(W))),
            o=Output(U.w(W))
        )
        m = matrixMul(1, len(w), 1).io
        m.a <<= io.i

        m.b <<= w
        io.o <<= m.o[0][0] + b

    return Unit()


def main():
    # 得到权重向量为[3, 4, 5, 6, 7, 8, 9, 10]，偏移量为14的神经元电路
    n = neurons(weight([3, 4, 5, 6, 7, 8, 9, 10]), bias(14))
    f = Emitter.dump(Emitter.emit(n), "neurons.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
