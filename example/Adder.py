from pyhcl import *
from pyhcl.simulator import Simulator


class FullAdder(Module):
    io = IO(
        a=Input(Bool),
        b=Input(Bool),
        cin=Input(Bool),
        sum=Output(Bool),
        cout=Output(Bool),
    )

    # Generate the sum
    a_xor_b = io.a ^ io.b
    io.sum <<= a_xor_b ^ io.cin

    # Generate the carry
    a_and_b = io.a & io.b
    b_and_cin = io.b & io.cin
    a_and_cin = io.a & io.cin
    io.cout <<= a_and_b | b_and_cin | a_and_cin


def adder(n: int):
    class Adder(Module):
        io = IO(
            a=Input(U.w(n)),
            b=Input(U.w(n)),
            cin=Input(Bool),
            sum=Output(U.w(n)),
            cout=Output(Bool),
        )

        FAs = [FullAdder().io for _ in range(n)]
        carry = Wire(Vec(n + 1, Bool))
        sum = Wire(Vec(n, Bool))

        carry[0] <<= io.cin

        for i in range(n):
            FAs[i].a <<= io.a[i]
            FAs[i].b <<= io.b[i]
            FAs[i].cin <<= carry[i]
            carry[i + 1] <<= FAs[i].cout
            sum[i] <<= FAs[i].sum

        io.sum <<= CatVecH2L(sum)
        io.cout <<= carry[n]

    return Adder()


def main():
    s = Simulator(adder(8))
    handler = s.handler

    # ---------- Simulation begin ---------- #
    s.start()

    for i in range(16):
        s.poke(handler.io.a, i)
        s.poke(handler.io.b, i + 1)
        s.poke(handler.io.cin, i % 2)
        s.step()
        s.peek(handler.io.sum)
        s.peek(handler.io.cout)

    s.term()
    # ---------- Simulation end ---------- #


if __name__ == '__main__':
    main()
