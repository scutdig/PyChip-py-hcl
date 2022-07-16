from pyhcl.simulator.simlite_verilog import Simlite
import random


# 每次给输入端口赋值, 跑一个时间单位
def test_step(s):
    s.start()
    s.step([0, 0, 20, 20])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([1, 0, 15, 10])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([0, 0, 1000, 1])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([1, 0, 999, 201])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.stop()


def test_task(s):
    tasks = []
    tasks.append([0, 0, 20, 20])
    tasks.append([1, 0, 15, 10])
    tasks.append([0, 0, 1000, 1])
    tasks.append([1, 0, 999, 201])

    s.start_task('Top', tasks)


def randomInput(ifn):
    fd = open(ifn, "w")
    instr = ""
    for i in range(100):
        instr += "0 0 0 " + str(random.randint(1, 2000)) + ' ' + str(random.randint(1, 2000)) + "\n"
    instr = instr + "-1\n"
    fd.write(instr)
    fd.close()


def test_file(s, num):
    ifn = f"../myTests/tmp/Top_inputs" + str(num)
    ofn = f"../myTests/tmp/Top_outputs" + str(num)
    randomInput(ifn)
    s.start(mode="task", ofn=ofn, ifn=ifn)
    pass


def main():
    top_module_name = 'Top.v'
    dut_path = 'myTests/tmp/dut/'
    s1 = Simlite(top_module_name, dut_path, debug=True)
    s2 = Simlite(module=s1)

    test_file(s1, 1)
    test_file(s2, 2)

    s1.close()
    s2.close()


if __name__ == '__main__':
    main()

