from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import Simlite, DpiConfig
from queue import Queue


class Add(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        in2=Input(U.w(32)),
        out=Output(U.w(32))
    )


@sv(a=DataType.UInt, b=DataType.UInt, return_type=Reference(x=DataType.UInt))
def fn(a, b):
    return a + b


addpysvmodule(Add, fn)      # 黑盒与函数     # 转换得到.sv/bbox/Add.sv，（SV里调用python函数）
compile_and_binding_all()   # 编译得到共享库 到.build文件夹下, 生成 SV binding文件 （.sv/pkg/pysv_pkg.sv）


class Top(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        c=Output(U.w(32))
    )

    add = Add()
    add.io.in1 @= io.a
    add.io.in2 @= io.b
    io.c @= add.io.out


from random import randint


def main():
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), dpiconfig=cfg, debug=True)
    s.start()
    s.step([20, 20])
    print("time: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([15, 10])
    print("time: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([1000, 1])
    print("time: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([999, 201])

    # tasks = []
    # tasks.append([11, 12])
    # tasks.append([12, 13])
    # tasks.append([13, 14])
    # s.start_task('Top', tasks)

    # s.start()
    # s.step([15, 10])
    # s.step([1000, 1])
    # s.step([999, 201])
    s.close()


if __name__ == '__main__':
    main()
