import tempfile
import os

from py_hcl import Module, IO, Input, Bool, Output


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


def main():
    tmp_dir = tempfile.mkdtemp()
    path = os.path.join(tmp_dir, "full_adder.fir")

    FullAdder.compile_to_firrtl(path)

    with open(path) as f:
        print(f.read())

    os.remove(path)
    os.removedirs(tmp_dir)


if __name__ == '__main__':
    main()
