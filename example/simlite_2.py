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


from random import randint


def main():

    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))
    s = Simlite(Top(), debug=True)
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
