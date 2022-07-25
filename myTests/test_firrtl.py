from pyhcl import *
from pyhcl.util.firrtltools import addfirrtlmodule
from pyhcl.simulator import Simlite
import random


class Add(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        in2=Input(U.w(32)),
        out=Output(U.w(32)),
    )


fd = open(f"myTests/tmp/firrtl/Add.fir", "r")
firrtl_code = "".join(fd.readlines())
# print(firrtl_code)
addfirrtlmodule(Add, firrtl_code)


class M(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        c=Output(U.w(32)),
    )

    bbox = Add()
    bbox.io.in1 @= io.a
    bbox.io.in2 @= io.b
    io.c @= bbox.io.out


# 每次给输入端口赋值, 跑一个时间单位
def test_step(s):
    s.start()

    s.step([20, 20])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([15, 10])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([1000, 1])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([999, 201])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))

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
    s = Simlite(M())

    # test_step(s)
    # test_task(s)
    test_file(s)

    s.close()
