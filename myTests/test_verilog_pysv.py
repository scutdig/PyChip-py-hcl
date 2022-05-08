from pyhcl.util.pysvtools import compile_and_binding_all_func
from pyhcl.simulator.simlite_verilog import Simlite, DpiConfig
from pysv import sv, DataType, Reference
import random


@sv(a=DataType.UInt, b=DataType.UInt, return_type=Reference(x=DataType.UInt))
def fn(a, b):
    return a + b


# 传入函数列表
# 编译得到共享库 到.build文件夹下, 生成 SV binding文件 （.sv/pkg/pysv_pkg.sv）
compile_and_binding_all_func([fn])


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


def test_file(s):
    ifn = f"../myTests/tmp/Top_inputs"
    ofn = f"../myTests/tmp/Top_outputs"
    randomInput(ifn)
    s.start(mode="task", ofn=ofn, ifn=ifn)
    pass


def main():
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Add.fir"))
    top_module_name = 'Top.v'
    dut_path = 'myTests/tmp/dut_pysv/'
    # 创建 DpiConfig对象，传入调用Python函数的SV文件名列表
    cfg = DpiConfig(['Add.sv'])
    s = Simlite(top_module_name, dut_path, dpiconfig=cfg, debug=True)

    # test_step(s)
    # test_task(s)
    test_file(s)

    s.close()


if __name__ == '__main__':
    main()

