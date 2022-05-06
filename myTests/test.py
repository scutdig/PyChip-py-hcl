from typing import Type, Union, Dict


class IO:
    _ios: Dict[str, int]

    def __init__(self, **kwargs):
        self._ios = kwargs


class Add:
    io = IO(
        in1=3,
        in2=4,
        out=5
    )

import re
# 解析verilog代码, 返回输入端口名列表 和 输出端口名列表
def verilog_parse(dut_path, top_module_name):
    top_module_path = dut_path + top_module_name
    print(top_module_path)
    with open(top_module_path, "r") as file:
        verilog_code = file.readlines()
        verilog_code = ''.join(verilog_code)
        # module_name_match = re.compile(r"module\s*([a-zA-Z0-9_]+)")

        # 匹配输入端口        input clock, input [31:0] io_a
        input_port_match = re.compile(r"input\s*(reg|wire)*\s*(\[[0-9]+\:[0-9]+\]*)*\s*([a-zA-Z0-9_]+)")
        # 匹配输出端口        output [31:0] io_c
        output_port_match = re.compile(r"output\s*(reg|wire)*\s*(\[[0-9]+\:[0-9]+\]*)*\s*([a-zA-Z0-9_]+)")

        # module_name = re.search(module_name_match, verilog_code).group(1)
        input_ports = re.findall(input_port_match, verilog_code)
        output_ports = re.findall(output_port_match, verilog_code)
        try:
            # 输入端口名列表
            input_ports_name = [input_port[2] for input_port in input_ports]
            # 输出端口名列表
            output_ports_name = [output_port[2] for output_port in output_ports]
            # print(input_ports)
            # print(output_ports)
            print(input_ports_name)
            print(output_ports_name)
            # print(verilog_code)
        except:
            print("can't find input or output ports")
    return input_ports_name, output_ports_name


if __name__ == '__main__':
    verilog_parse('./tmp/dut/', 'Top.v')
    print('dur.v'.split('.')[0])
    # print(Add.io)
    # print(Add.io._ios)
    # print(Add().io._ios)
    # print(Add().io.value._ios)

    path = './tmp/test'
    cnt = 0
    # with open(path, "a") as file:
    #     while file:
    #         line = file.readline().strip(' ')
    #         if line == '':
    #             break
    #         print(line)
    #         cnt = cnt + 1

    # f = open(path, "a")
    # inputs = [[2000, 230032]] * 4
    # print(inputs)
    # print(cnt)
    a = {'a': 'b', 'b': 'c'}
    if 'c' in a:
        print("XX")
        pass
    input_data = ['0111', '0011']
    input_data = [int(k, base=2) for k in input_data]
    print(input_data)


