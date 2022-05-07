from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import Simlite, DpiConfig
import random


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
    add.io.in1 <<= io.a
    add.io.in2 <<= io.b
    io.c <<= add.io.out


# 每次给输入端口赋值, 跑一个时间单位
def test_step(s):
    s.start()

    s.step([20, 20])
    print("time: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([15, 10])
    print("time: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([1000, 1])
    print("time: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([999, 201])

    s.stop()


def test_task(s):
    tasks = []
    tasks.append([20, 20])
    tasks.append([15, 10])
    tasks.append([1000, 1])
    tasks.append([999, 201])

    s.start_task('Top', tasks)


def randomInput(ifn):
    fd = open(ifn, "w")
    instr = ""
    for i in range(100):
        instr += "0 " + str(random.randint(1, 2000)) + ' ' + str(random.randint(1, 2000)) + "\n"
    instr = instr + "-1\n"
    fd.write(instr)
    fd.close()


def test_file(s):
    ifn = f"../myTests/tmp/Top_inputs"
    ofn = f"../myTests/tmp/Top_outputs"
    randomInput(ifn)
    s.start(mode="task", ofn=ofn, ifn=ifn)
    pass


def main():
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), dpiconfig=cfg, debug=True)

    test_step(s)
    # test_task(s)
    # test_file(s)

    s.close()


if __name__ == '__main__':
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), dpiconfig=cfg, debug=True)
    s.start()
    s.step([20, 20])
    s.step([15, 10])
    s.step([1000, 1])
    s.step([999, 201])
    s.close()
