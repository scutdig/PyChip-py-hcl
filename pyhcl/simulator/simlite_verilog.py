import os
import subprocess
import re


class DpiConfig(object):
    def __init__(self, pysv_li, pkg_sv_path=".sv/pkg/pysv_pkg.sv", lib_path=".build/libpysv.so"):
        self.sv = pkg_sv_path
        self.lib = lib_path
        self.bname = " ".join(pysv_li)
        ...


class Simlite(object):
    # init for fork method
    # 根据传入的Simlite对象实例，深度复制得到新的Simlite对象实例
    def __fork_init(self, other):
        import copy
        self.top_module_name = other.top_module_name
        self.dut_path = other.dut_path
        self.dpiconfig = other.dpiconfig
        if hasattr(other, "efn"):
            self.efn = other.efn
        self.inputs = copy.deepcopy(other.inputs)
        self.outputs = copy.deepcopy(other.outputs)
        self.results = copy.deepcopy(other.outputs)
        self.cnt = copy.deepcopy(other.cnt)
        self.dut_name = copy.deepcopy(other.dut_name)

        # recover the status base on self.steps
        self.steps = []
        self.debug = False

        # 开始仿真
        self.start()
        for inputs in other.steps:
            self.step(inputs)
        assert (self.steps == other.steps)

        self.debug = other.debug
        self.name = other.name + "_" + str(other.fork_cnt)
        other.fork_cnt += 1

    # dpiconfig对象
    # self.sv = pkg_sv_path     # .sv/pkg/pysv_pkg.sv
    # self.lib = lib_path       # .build/libpysv.so
    # self.bname = " ".join(pysv_li)  # pysv_li存放调用了python函数的SV列表 (Add.sv)
    def __init__(self, top_module_name='', dut_path='', harness_code=None, dpiconfig: DpiConfig = None, debug=False, name="sim0", module=None):
        self.raw_in = None
        self.efn = None
        self.ofn = None
        self.ifn = None
        self.dut_path = dut_path
        self.top_module_name = top_module_name
        # module为Simlite对象实例
        if isinstance(module, Simlite):
            self.__fork_init(module)
        else:
            self.dpiconfig = dpiconfig
            # 输入端口名列表
            self.inputs = []
            self.inputs_values = []
            # 输出端口名列表
            self.outputs = []
            # 结果列表
            self.results = []
            # 计数器
            self.cnt = 0
            # 步骤列表
            self.steps = []
            # 仿真名
            self.name = name

            self.debug = debug
            self.fork_cnt = 0

            self.inputs, self.outputs = self.verilog_parse(dut_path, top_module_name)

            # dut_name: Top     top_module_name: Top.v
            self.dut_name = top_module_name.split('.')[0]         # 模块名

            # 通过harness代码开始仿真
            if harness_code:
                self.compile(harness_code)
            else:
                # 传入module_name和ports生成harness代码，然后仿真
                self.compile(self.codegen(self.dut_name))

    # 解析verilog代码, 返回输入端口名列表 和 输出端口名列表
    def verilog_parse(self, dut_path, top_module_name):
        dut_name = top_module_name.split('.')[0]  # 模块名
        top_module_path = dut_path + top_module_name
        # print(top_module_path)
        module_begin_match = r"module\s*([a-zA-Z0-9_]+)"
        # 匹配输入端口        input clock, input [31:0] io_a
        input_port_match = r"input\s*(reg|wire)*\s*(\[[0-9]+\:[0-9]+\]*)*\s*([a-zA-Z0-9_]+)"
        # 匹配输出端口        output [31:0] io_c
        output_port_match = r"output\s*(reg|wire)*\s*(\[[0-9]+\:[0-9]+\]*)*\s*([a-zA-Z0-9_]+)"
        current_module_name = ''
        input_ports_name = []
        output_ports_name = []
        with open(top_module_path, "r") as verilog_file:
            while verilog_file:
                verilog_line = verilog_file.readline().strip(' ')  # 读取一行
                # print(verilog_line)
                if verilog_line == "":  # 注：如果是空行，为'\n'
                    break

                module_begin = re.search(module_begin_match, verilog_line)

                if module_begin:
                    current_module_name = module_begin.group(1)
                    # print(current_module_name)

                if current_module_name == dut_name:
                    input_port = re.search(input_port_match, verilog_line)
                    output_port = re.search(output_port_match, verilog_line)
                    if input_port:
                        # 输入端口名列表
                        input_ports_name.append(input_port.group(3))
                    if output_port:
                        # 输出端口名列表
                        output_ports_name.append(output_port.group(3))
        # print(dut_name)
        # print(input_ports_name)
        # print(output_ports_name)
        return input_ports_name, output_ports_name

    # --timescale <timescale>     Sets default timescale
    # --timescale <timeunit>/<timeprecision>
    def setTimeScale(self, timescale):
        pass

    def stop(self):
        instr = '-1'.encode(encoding="utf-8") + b'\n'
        self.p.stdin.write(instr)
        self.p.stdin.flush()

    def close(self):
        # 2表示标准错误stderr, >表示重定向 ，/dev/mull表示空设备
        # 2>/dev/nul,将标准错误重定向到空设备里，即不输出错误信息
        # 追加 2>/dev/null 在命令末尾，表示：把错误输出到 “黑洞”
        os.system("cd .. && rm -r .sv .fir .build 2>/dev/null")
        # self.p.kill()
        # pass

    # 传入harness代码，调用firrtl命令得到verilog代码，调用verilater最终得到V{dut_name}
    def compile(self, harness_code):
        print("\n\n---------------------verilator build info--------------------------\n")
        dpiconfig = self.dpiconfig

        # 在当前目录创建simulation文件夹
        try:
            os.mkdir("simulation")
        except FileExistsError:
            pass

        # 把所有dut文件复制到simulation文件夹下
        os.system("cp {}* ./simulation/".format(self.dut_path))

        # 在simulation文件夹下创建dut_name-harness.cpp，写入harness代码
        with open(f"./simulation/{self.dut_name}-harness.cpp", "w+") as f:
            f.write(harness_code)

        # vfn = "{}.v".format(self.dut_name)              # {dut_name}.v
        vfn = self.top_module_name
        hfn = "{}-harness.cpp".format(self.dut_name)    # {dut_name}-harness.cpp
        mfn = "V{}.mk".format(self.dut_name)            # V{dut_name}.mk
        efn = "V{}".format(self.dut_name)               # V{dut_name}

        # dpi
        if self.dpiconfig:
            # dpiconfig对象
            # self.sv = pkg_sv_path     # .sv/pkg/pysv_pkg.sv
            # self.lib = lib_path       # .build/libpysv.so
            # self.bname = " ".join(pysv_li)  # pysv_li存放调用了python函数的SV列表 (Add.sv)
            pysv_pkg = "{}_pysv_pkg.sv".format(self.dut_name)       # {dut_name}_pysv_pkg.sv
            pysv_lib = "libpysv_{}.so".format(self.dut_name)        # libpysv_{dut_name}.so

            # cp .sv/pkg/pysv_pkg.sv ./simulation/{dut_name}_pysv_pkg.sv        # 由各python函数生成得到的SV binding文件
            os.system("cp {} ./simulation/{}_pysv_pkg.sv".format(dpiconfig.sv, self.dut_name))
            # cp .build/libpysv.so ./simulation/libpysv_{dut_name}.so           # 由各python函数编译得到的共享库
            os.system("cp {} ./simulation/libpysv_{}.so".format(dpiconfig.lib, self.dut_name))
            
            # 转换目录到./simulation文件夹下
            os.chdir("./simulation")

            # Using verilator backend
            # --cc                        Create C++ output
            # --trace                     Enable waveform creation
            # --exe                       Link to create executable
            # --prefix <topname>          Name of top level class
            # --top-module <topname>      Name of top level input module
            # .so为 与 Verilog 代码链接的可选对象或库文件
            # In the verilator command, include the shared library and the generated binding file
            # verilator --cc --trace --exe --prefix VTop --top-module Top Top_pysv_pkg.sv {bbx} libpysv_Top.so Top-harness.cpp
            # verilator --cc --trace --exe --prefix VTop --top-module Top Top_pysv_pkg.sv Add.sv Top.v libpysv_Top.so Top-harness.cpp
            print(
                "verilator --cc --trace --exe --prefix {prefix} --top-module {top} {pkg} {bbx} {vfn} {lib} {hfn}" \
                    .format(top=self.dut_name, bbx=dpiconfig.bname, vfn=vfn, hfn=hfn, pkg=pysv_pkg, lib=pysv_lib,
                            prefix=efn))
            os.system(
                "verilator --cc --trace --exe --prefix {prefix} --top-module {top} {pkg} {bbx} {vfn} {lib} {hfn}" \
                    .format(top=self.dut_name, bbx=dpiconfig.bname, vfn=vfn, hfn=hfn, pkg=pysv_pkg, lib=pysv_lib,
                            prefix=efn))
            # cp libpysv_Top.so ./obj_dir/
            os.system("cp {} ./obj_dir/".format(pysv_lib))

        else:
            # 改变当前工作目录到指定的路径--simulation
            os.chdir("./simulation")

            # Using verilator backend
            # 传入verilog代码和harness代码，使用verilator进行仿真
            # --cc                        Create C++ output
            # --trace                     Enable waveform creation
            # --exe                       Link to create executable
            # verilator --cc {dut_name}.v --trace --exe {dut_name}-harness.cpp
            print("verilator --cc {vfn} --trace --exe {hfn}".format(vfn=vfn, hfn=hfn))
            os.system(
                "verilator --cc {vfn} --trace --exe {hfn}".format(vfn=vfn, hfn=hfn))

        # make -j -C ./obj_dir -f V{dut_name}.mk V{dut_name}
        os.system(
            "make -j -C ./obj_dir -f {mfn} {efn}".format(mfn=mfn, efn=efn))

        # Run simulation backend program
        """
        if dpiconfig:
            os.system("LD_LIBRARY_PATH=. ./obj_dir/{}&".format(efn))
        else:
            os.system("./obj_dir/{}&".format(efn))
        """
        self.efn = efn      # V{dut_name}

    # 开启仿真，默认模式为ia
    def start(self, mode="ia", ofn=None, ifn=None):
        env = None
        if self.dpiconfig:
            # 确保 libpysv.so（共享库） 在 LD_LIBRARY_PATH 中--  pysv要求的
            env = {"LD_LIBRARY_PATH": "."}          # 环境变量
        if mode == "ia":
            args = [f"./obj_dir/{self.efn}"]        # ./obj_dir/V{dut_name}

            # 创建子进程执行./obj_dir/{dut_name}
            self.p = subprocess.Popen(args, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            self.dropinfo()
        elif mode == "task":
            args = [f"./obj_dir/{self.efn}"]        # ./obj_dir/V{dut_name}
            infile = open(ifn, "r")
            outfile = open(ofn, "w")
            # subprocess 模块允许我们启动一个新进程，并连接到它们的输入/输出/错误管道，从而获取返回值。
            # Popen 是 subprocess的核心，子进程的创建和管理都靠它处理
            # args：shell命令，可以是字符串或者序列类型（如：list，元组）
            # env：用于指定子进程的环境变量。如果 env = None，子进程的环境变量将从父进程中继承
            # shell：如果该参数为 True，将通过操作系统的 shell 执行指定的命令
            # stdin、stdout 和 stderr：子进程的标准输入、输出和错误句柄
            # 创建子进程执行./obj_dir/VAdder
            # self.p = subprocess.Popen(args, env=env, shell=True, stdin=subprocess.PIPE, stdout=outfile)
            self.p = subprocess.Popen(args, env=env, stdin=infile, stdout=outfile)

    # 读掉stdout缓冲区里的5行info
    def dropinfo(self):
        for i in range(5):
            self.p.stdout.readline()
        if self.debug:
            print("\n\n--------------------------sim result---------------------------")

    # 传入整个任务tsk，开始仿真（task模式）      name为模块名，tsk为二维列表（包含每一次的输入端口列表值）
    def start_task(self, name, tsk):
        try:
            os.mkdir("tmp")
        except FileExistsError:
            pass
        # input file
        ifn = f"./tmp/{name}_inputs"
        ofn = f"./tmp/{name}_outputs"
        fd = open(ifn, "a")
        instr = ""
        for inputs in tsk:
            # 一次输入端口值列表
            inputs = [str(x) for x in inputs]
            # 输入端口值--str
            self.raw_in = " ".join(inputs)
            self.raw_in = "0 " + self.raw_in        # 0表示状态值，状态值小于0会退出
            instr += self.raw_in + "\n"
        # 所有输入端口值，每一次以\n分隔
        instr += "-1\n"
        # 将tsk（整个任务，包含每一次的输入端口列表值）传入ifn（输入文件）
        fd.write(instr)
        fd.close()
        # 传入输入文件和输出文件，开始仿真
        self.start("task", ofn, ifn)

    # 传入输入端口值列表
    def step(self, inputs):
        # 每一步存入steps列表
        self.steps.append(inputs)
        self.inputs_values = inputs
        # 输入端口值列表
        inputs = [str(x) for x in inputs]
        # 输入端口值--str
        self.raw_in = " ".join(inputs)
        self.raw_in = "0 " + self.raw_in
        instr = self.raw_in.encode(encoding="utf-8") + b'\n'

        # 将输入端口值--str写入子进程的标准输入stdin缓冲区--传入inputs数组
        self.p.stdin.write(instr)
        # 刷新stdin缓冲区, 即将缓冲区中的数据立刻写入
        self.p.stdin.flush()
        # 读取子进程的标准输出stdout里的内容--即outputs数组的值
        line = self.p.stdout.readline()
        # 刷新stdout缓冲区
        self.p.stdout.flush()

        # 从outputs数组中读取的结果--输出端口值
        self.raw_res = str(line, encoding="utf-8").strip()
        strs = self.raw_res.split(" ")

        # 结果列表
        res = [int(x) for x in strs]
        self.results = res

        # debug模式
        if self.debug:
            self.pprint()

        # 计数器值加一
        self.cnt += 1
        return res

    # 输出仿真相关值--输入端口值、输出端口值
    def pprint(self):
        print("")
        # 仿真名   计数器值  IN：   输入端口值
        # 仿真名   计数器值  OUT：   输出端口值
        print(f"[{self.name}\t\t{self.cnt}]IN  : {self.raw_in}")
        print(f"[{self.name}\t\t{self.cnt}]OUT : {self.raw_res}")

    def getRes(self):
        return self.results

    # 传入module_name和ports，生成harness代码
    def codegen(self, name):
        tempfile = """#include "V{modname}.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <vector>
#include <iostream>
#include <cstdio>

vluint64_t main_time = 0;   // See comments in first example
const vluint64_t sim_time = 1024;
double sc_time_stamp() {{ return main_time; }}

std::vector<unsigned long long> inputs, outputs;

#define INN {innum}
#define OUTN {outnum}
int status = 0;

void ioinit(){{
    setvbuf(stdout,0,_IONBF, 0);
    setvbuf(stdin,0,_IONBF, 0);
    setvbuf(stderr,0,_IONBF, 0);
    inputs.resize(INN);
    outputs.resize(OUTN);
    return;
}}

void input_handler(){{
    std::cin>>status;
    if(status==-1)
        return;
    for(int i = 0; i < INN; i++){{
        std::cin>>inputs[i];
    }}
    return;
}}

void output_handler(){{
    for(int i = 0; i < OUTN; i++){{
        std::cout<<outputs[i]<<" ";
    }}
    std::cout<<std::endl;
    return;
}}

int main(int argc, char** argv, char** env) {{
    Verilated::commandArgs(argc, argv);
    ioinit();
    
    V{modname}* top = new V{modname};
    
    Verilated::internalsDump();  // See scopes to help debug
    Verilated::traceEverOn(true);
    
    VerilatedVcdC* tfp = new VerilatedVcdC;
    top->trace(tfp, 99);
    tfp->open("wave.vcd");

    while (!Verilated::gotFinish()) {{
        input_handler();
        if(status==-1) break;
        //get inputs
{inputs_init}
        top->eval();
        tfp->dump(main_time);
{outputs_log}
        //get output
        output_handler();
        main_time++;
    }}
    top->final();
    tfp->close();
    delete top;
    return 0;
}}""".format(modname=name, innum=len(self.inputs), outnum=len(self.outputs), inputs_init=self.handle_inputs(),
             outputs_log=self.handle_outputs())
        return tempfile

    # 处理input端口，得到对应的harness代码  # 用inputs数组对输入端口进行赋值
    def handle_inputs(self):
        res = ""
        taps = "        "
        i = 0
        for n in self.inputs:
            res += taps + f"top->{n} = inputs[{i}];\n"       # 对输入端口进行赋值
            i += 1
        return res

    # 处理output端口，得到对应的harness代码 # 对输出端口进行取值，放入outputs数组
    def handle_outputs(self):
        res = ""
        taps = "        "
        i = 0
        for n in self.outputs:
            res += taps + f"outputs[{i}] = top->{n};\n"      # 对输出端口进行取值
            i += 1
        return res
