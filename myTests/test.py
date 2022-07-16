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


# 解析FIRRTL代码, 返回输入端口名列表 和 输出端口名列表
def firrtl_parse(firrtl_path):
    circuit_begin_match = r"circuit\s*([a-zA-Z0-9_]+)"
    module_begin_match = r"module\s*([a-zA-Z0-9_]+)"
    input_port_match = r"input\s*([a-zA-Z0-9_]+)"
    output_port_match = r"output\s*([a-zA-Z0-9_]+)"
    input_ports_name = []
    output_ports_name = []
    top_module_name = '0'
    current_module_name = '1'
    with open(firrtl_path, "r") as firrtl_file:
        while firrtl_file:
            firrtl_line = firrtl_file.readline().strip(' ')  # 读取一行
            # print(firrtl_line)
            if firrtl_line == "":           # 注：如果是空行，为'\n'
                break

            circuit_begin = re.search(circuit_begin_match, firrtl_line)
            module_begin = re.search(module_begin_match, firrtl_line)

            if circuit_begin:
                top_module_name = circuit_begin.group(1)
                # print(top_module_name)

            if module_begin:
                current_module_name = module_begin.group(1)
                # print(current_module_name)

            if current_module_name == top_module_name:
                input_port = re.search(input_port_match, firrtl_line)
                output_port = re.search(output_port_match, firrtl_line)
                if input_port:
                    input_ports_name.append(input_port.group(1))
                if output_port:
                    output_ports_name.append(output_port.group(1))
    print(top_module_name)
    print(input_ports_name)
    print(output_ports_name)
    return top_module_name, input_ports_name, output_ports_name


# 解析verilog代码, 返回输入端口名列表 和 输出端口名列表
def verilog_parse(dut_path, top_module_name):
    dut_name = top_module_name.split('.')[0]         # 模块名
    top_module_path = dut_path + top_module_name
    # print(top_module_path)
    module_begin_match = r"module\s*([a-zA-Z0-9_]+)"

    input_port_match = r"input\s*(reg|wire)*\s*(\[[0-9]+\:[0-9]+\]*)*\s*([a-zA-Z0-9_]+)"
    output_port_match = r"output\s*(reg|wire)*\s*(\[[0-9]+\:[0-9]+\]*)*\s*([a-zA-Z0-9_]+)"

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
                    input_ports_name.append(input_port.group(3))
                if output_port:
                    output_ports_name.append(output_port.group(3))
    # print(dut_name)
    # print(input_ports_name)
    # print(output_ports_name)
    return input_ports_name, output_ports_name


if __name__ == '__main__':

    # verilog_parse('./tmp/dut/', 'Top.v')
    verilog_parse('../simulation/', 'M.v')
    # firrtl_parse('./tmp/firrtl/M.fir')


