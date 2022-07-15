from pyhcl import *
from pyhcl.simulator import Simlite


class HalfAdder(Module):
    io = IO(
        a=Input(U.w(1)),
        b=Input(U.w(1)),
        s=Output(U.w(1)),
        cout=Output(U.w(1))
    )
    # 填充完整输出端口s以及cout的逻辑，例如：
    io.s <<= io.a ^ io.b
    io.cout <<= io.a & io.b


def main():
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(HalfAdder()), "HalfAdder.fir"))
    # cfg = DpiConfig()
    s = Simlite(HalfAdder())
    # s.start()
    # s.step([20, 20])
    # s.step([15, 10])
    # s.step([1000, 1])
    # s.step([999, 201])
    # s.close()


# 生成Verilog文件
if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(HalfAdder()), "HalfAdder.fir"))
    # cfg = DpiConfig()
    s = Simlite(HalfAdder())
    s.start()
    s.step([20, 20])
    s.step([15, 10])
    s.step([1000, 1])
    s.step([999, 201])
    s.close()
