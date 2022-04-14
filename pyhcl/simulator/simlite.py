import os
import subprocess

from pyhcl import *
from ..simulator import DpiConfig


class Simlite(object):
    # init for fork method
    def __fork_init(self, other):
        import copy
        self.low_module = other.low_module
        self.dpiconfig = other.dpiconfig
        if (hasattr(other, "efn")):
            self.efn = other.efn
        self.inputs = copy.deepcopy(other.inputs)
        self.outputs = copy.deepcopy(other.outputs)
        self.results = copy.deepcopy(other.outputs)
        self.cnt = copy.deepcopy(other.cnt)
        self.dut_name = copy.deepcopy(other.dut_name)

        # recover the status base on self.steps
        self.steps = []
        self.debug = False
        self.start()
        for inputs in other.steps:
            self.step(inputs)
        assert (self.steps == other.steps)

        self.debug = other.debug
        self.name = other.name + "_" + str(other.fork_cnt)
        other.fork_cnt += 1

    def __init__(self, module, harness_code=None, dpiconfig: DpiConfig = None, debug=False, name="sim0"):
        self.raw_in = None
        self.efn = None
        self.ofn = None
        self.ifn = None
        if isinstance(module, Simlite):
            self.__fork_init(module)
        else:
            self.low_module = Emitter.elaborate(module)
            self.dpiconfig = dpiconfig
            module_name = self.low_module.main
            # ports = next(m.typ for m in low_module.modules if m.name == module_name)
            ports = module.io.value._ios

            self.inputs = []
            self.outputs = []
            self.results = []
            self.cnt = 0
            self.steps = []
            self.name = name

            self.debug = debug
            self.fork_cnt = 0

            for k, v in ports.items():
                if (type(v) == Input):
                    self.inputs.append(k)
                elif (type(v) == Output):
                    self.outputs.append(k)

            self.dut_name = module_name
            if harness_code:
                self.compile(harness_code)
            else:
                self.compile(self.codegen(module_name, ports))

    def close(self):
        os.system("cd .. && rm -r .sv .fir .build 2>/dev/null")

    def compile(self, harness_code):
        print("\n\n---------------------verilator build info--------------------------\n")
        dpiconfig = self.dpiconfig
        try:
            os.mkdir("simulation")
        except FileExistsError:
            pass

        with open(f"./simulation/{self.dut_name}-harness.cpp", "w+") as f:
            f.write(harness_code)

        # 调用FIRRTL工具链
        # with open(f"./simulation/{self.dut_name}.fir", "w+") as f:
        #     f.write(self.low_module.serialize())

        # os.system(
        #     f"firrtl -i ./simulation/{self.dut_name}.fir -o ./simulation/{self.dut_name}.v -X verilog")
        
        # # 调用PyHCL编译链
        with open(f"./simulation/{self.dut_name}.v", "w+") as f:
            f.write(Verilog(self.low_module).emit())

        vfn = "{}.v".format(self.dut_name)
        hfn = "{}-harness.cpp".format(self.dut_name)
        mfn = "V{}.mk".format(self.dut_name)
        efn = "V{}".format(self.dut_name)

        # dpi
        if self.dpiconfig:
            pysv_pkg = "{}_pysv_pkg.sv".format(self.dut_name)
            pysv_lib = "libpysv_{}.so".format(self.dut_name)

            os.system("cp {} ./simulation/{}_pysv_pkg.sv".format(dpiconfig.sv, self.dut_name))
            os.system("cp {} ./simulation/libpysv_{}.so".format(dpiconfig.lib, self.dut_name))
            os.system("cp {}* ./simulation/".format(dpiconfig.bdir))

            os.chdir("./simulation")
            # Using verilator backend
            os.system(
                "verilator --cc --trace --exe --prefix {prefix} --top-module {top} {pkg} {bbx} {vfn} {lib} {hfn}" \
                    .format(top=self.dut_name, bbx=dpiconfig.bname, vfn=vfn, hfn=hfn, pkg=pysv_pkg, lib=pysv_lib,
                            prefix=efn))
            os.system("cp {} ./obj_dir/".format(pysv_lib))

        else:
            os.chdir("./simulation")
            # Using verilator backend
            os.system(
                "verilator --cc {vfn} --trace --exe {hfn}".format(vfn=vfn, hfn=hfn))

        os.system(
            "make -j -C ./obj_dir -f {mfn} {efn}".format(mfn=mfn, efn=efn))

        # Run simulation backend program
        """
        if dpiconfig:
            os.system("LD_LIBRARY_PATH=. ./obj_dir/{}&".format(efn))
        else:
            os.system("./obj_dir/{}&".format(efn))
        """
        self.efn = efn

    def start(self, mode="ia", ofn=None, ifn=None):
        env = None
        if self.dpiconfig:
            env = {"LD_LIBRARY_PATH": "."}
        if mode == "ia":
            args = [f"./obj_dir/{self.efn}"]
            self.p = subprocess.Popen(args, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            self.dropinfo()
        elif mode == "task":
            args = [f"./obj_dir/{self.efn}"]
            infile = open(ifn, "r")
            outfile = open(ofn, "a")
            self.p = subprocess.Popen(args, env=env, shell=True, stdin=infile, stdout=outfile)

    def dropinfo(self):
        for i in range(5):
            self.p.stdout.readline()
        if self.debug:
            print("\n\n--------------------------sim result---------------------------")

    def start_task(self, name, tsk):
        # input file
        ifn = f"/tmp/{name}_inputs"
        ofn = f"/tmp/{name}_outputs"
        fd = open(ifn, "a")
        instr = ""
        for inputs in tsk:
            inputs = [str(x) for x in inputs]
            self.raw_in = " ".join(inputs)
            self.raw_in = "0 " + self.raw_in
            instr += self.raw_in + "\n"
        instr += "-1\n"
        fd.write(instr)
        fd.close()
        self.start("task", ofn, ifn)


    # TODO: pipe's output is empty.
    def step(self, inputs):
        self.steps.append(inputs)
        inputs = [str(x) for x in inputs]
        self.raw_in = " ".join(inputs)
        self.raw_in = "0 " + self.raw_in
        instr = self.raw_in.encode(encoding="utf-8") + b'\n'
        self.p.stdin.write(instr)
        self.p.stdin.flush()
        line = self.p.stdout.readline()
        self.p.stdout.flush()
        self.raw_res = str(line, encoding="utf-8").strip()
        strs = self.raw_res.split(" ")
        strs = [sx for sx in strs if sx != '']
        res = [int(x) for x in strs]
        self.results = res
        if self.debug:
            self.pprint()
        self.cnt += 1
        return res

    def pprint(self):
        print("")
        print(f"[{self.name}\t\t{self.cnt}]IN  : {self.raw_in}")
        print(f"[{self.name}\t\t{self.cnt}]OUT : {self.raw_res}")

    def codegen(self, name, ports):
        tempfile = """#include "V{modname}.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <vector>
#include <iostream>
#include <cstdio>

vluint64_t main_time = 0;   // See comments in first example
double sc_time_stamp() {{ return main_time; }}

std::vector<unsigned long long> inputs, outputs;

#define INN {innum}
#define OUTN {outnum}

void ioinit(){{
    setvbuf(stdout,0,_IONBF, 0);
    setvbuf(stdin,0,_IONBF, 0);
    setvbuf(stderr,0,_IONBF, 0);
    inputs.resize(INN);
    outputs.resize(OUTN);
    return;
}}

void input_handler(){{
    int status = 0;
    std::cin>>status;
    if(status<0)
        exit(0);
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
    top->trace(tfp, 0);
    tfp->open("wave.vcd");

    while (!Verilated::gotFinish()) {{
        input_handler();
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

    def handle_inputs(self):
        res = ""
        taps = "        "
        i = 0
        for n in self.inputs:
            res += taps + f"top->io_{n} = inputs[{i}];\n"
            i += 1
        return res

    def handle_outputs(self):
        res = ""
        taps = "        "
        i = 0
        for n in self.outputs:
            res += taps + f"outputs[{i}] = top->io_{n};\n"
            i += 1
        return res
