from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import Simlite, DpiConfig
from queue import Queue


class Top(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        c=Output(U.w(32))
    )

    io.c <<= io.a + io.b


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


def test_task(s):
    tasks = []
    tasks.append([20, 20])
    tasks.append([15, 10])
    tasks.append([1000, 1])
    tasks.append([999, 201])

    s.start_task('Top', tasks)


def test_file(s):
    ifn = f"../myTests/tmp/Top_inputs"
    ofn = f"../myTests/tmp/Top_outputs"
    s.start(mode="task", ofn=ofn, ifn=ifn)
    pass


def main():
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), debug=True)

    # test_step(s)
    # test_task(s)
    test_file(s)

    s.close()


if __name__ == '__main__':
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), debug=True)
    s.start()
    s.step([20, 20])
    s.step([15, 10])
    s.step([1000, 1])
    s.step([999, 201])
    s.close()
