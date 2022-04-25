import os
import sys
import re

# wip: better structured vcd reader
from injector.reader_base import ReaderBase


class VcdReader(ReaderBase):
    # 属性：vcd_path、excluded_sigs、replay_blocks、
    # 属性：scope_begin_match、scope_end_match、definitions_end_match、signal_match、simple_sig_match、vector_sig_match、dumpvars_match、new_time_match、sig_value_match
    # 父类属性：excluded_sigs、inputs_only、replay_blocks、signal_values、signal_changes
    def __init__(self, replay_blocks, wave_file, excluded_sigs, inputs_only):
        # 波形文件名（xxx.vcd）
        self.vcd_path = wave_file
        # 排除的信号
        self.excluded_sigs = excluded_sigs
        # 重新运行的模块
        self.replay_blocks = replay_blocks

        # ‘r’， raw string
        # ^	匹配字符串的开头
        # \s	匹配任意空白字符
        # re*	匹配0个或多个的表达式
        # [^...]	不在[]中的字符
        # .	匹配任意字符，除了换行符
        
        # 正则表达式
        # 匹配scope头          # 例：$scope module tb_top $end
        self.scope_begin_match = r"^\$scope\s*([^ ]+)\s*([^ ]+)\s*\$end"
        # 匹配scope尾          # 例：$upscope $end
        self.scope_end_match = r"\$upscope\s*\$end"
        # 匹配信号定义尾       # 例：$enddefinitions $end
        self.definitions_end_match = r"\$enddefinitions.*"

        # 匹配信号                # 例：$var reg       1 !    clk $end
        self.signal_match = r"\$var.*\$end"
        # 匹配简单信号            # 例：!    clk $end
        self.simple_sig_match = r"([^ ]+)\s*([a-zA-Z0-9_]+)\s*\$end"
        # 匹配信号数组            # 例：'    ctr [10:0] $end
        self.vector_sig_match = r"([^ ]+)\s*([a-zA-Z0-9_]+)\s*(\[[0-9]+\:[0-9]+\]*)\s*\$end"

        # 匹配dumpvars头           # 例：$dumpvars
        self.dumpvars_match = r"^\$dumpvars.*"
        # 匹配时间（#数字）        # 例：#10
        self.new_time_match = r"^#([0-9]+)"                             
        # 匹配信号值               # 例：b1 '  例：1&
        self.sig_value_match = r"^[b]{0,1}([zx10]+)[ ]{0,1}(.*)"

        super().__init__(replay_blocks, wave_file, excluded_sigs, inputs_only)

    # 从波形文件中提取
    def extract_values_from_wave(self, replay_blocks, excluded_sigs, inputs_only):
        # 得到信号值     字典{'信号':[(时间,'值'),...],...}
        self.sigs_values = {}       
        
        # 从vcd波形文件中提取（xxx.vcd）
        self.extract_vcd_file(self.vcd_path)

        return self.sigs_values

    # 从vcd波形文件中提取数据（xxx.vcd）
    def extract_vcd_file(self, valid_path):
        with open(valid_path, "r") as vcd_file:
            # 将信号名与vcd文件中字符名，一一对应
            self.sig_name_2_vcd_name = {}   # 信号名转vcd名
            self.vcd_name_2_sig_name = {}   # vcd名转信号名
            
            # 从vcd波形文件中提取前面scope部分
            self.extract_scopes(vcd_file)
            # print(self.sig_name_2_vcd_name)
            # 从vcd波形文件中提取信号值部分
            self.extract_sig_values(vcd_file)

    # 从当前scope(范围)中提取数据
    def extract_scopes(self, vcd_file, current_scope=""):
        while vcd_file:
            vcd_line = vcd_file.readline().strip(' ')  # 读取一行
            if vcd_line == "":           # 注：如果是空行，为'\n'
                return
            # re.match(pattern, string, flags=0)
            # re.match 方法从字符串的起始位置匹配一个模式，匹配成功，返回一个匹配的对象，否则返回 None
            # re.search(pattern, string, flags=0)
            # re.search 扫描整个字符串并返回第一个成功的匹配，否则返回 None
            
            # group() 同group（0）就是匹配正则表达式整体结果
            # group(1) 列出第一个括号匹配部分，group(2) 列出第二个括号匹配部分，group(3) 列出第三个括号匹配部分。
            
            # 匹配scope的头
            scope_begin = re.match(self.scope_begin_match, vcd_line)
            # 匹配scope的尾
            scope_end = re.match(self.scope_end_match, vcd_line)
            # 匹配信号
            sig = re.match(self.signal_match, vcd_line)
            # 匹配简单信号
            simple_sig = re.search(self.simple_sig_match, vcd_line)
            # 匹配信号数组
            vector_sig = re.search(self.vector_sig_match, vcd_line)
            # 匹配信号定义的结束
            definitions_end = re.search(self.definitions_end_match, vcd_line)

            # 信号定义的结束
            if definitions_end:
                if current_scope != "":   # 顶层
                    raise ValueError("Definitions terminated in the middle of scope: ", current_scope)
                return

            # scope的头
            if scope_begin:
                new_scope_name = scope_begin.group(2)   # 模块名
                prefix = current_scope + "." if current_scope != "" else ""
                # print("going into scope: ", prefix + new_scope_name)
                # 从scope模块中提取数据（递归）
                self.extract_scopes(vcd_file, prefix + new_scope_name)  # 从新模块中提取数据
            
            # scope的尾
            if scope_end:
                # print("going out of scope: ", current_scope)
                return  # 当前scope模块结束

            # 当前模块不用重新运行
            # if current_scope not in self.replay_blocks:
            #     # just read the lines   # 只是读行一直到scope_end
            #     continue

            # 简单信号
            if sig and simple_sig:
                self.update_sig_tables(current_scope, simple_sig)   # 更新信号表

            # 信号数组
            if sig and vector_sig:
                self.update_sig_tables(current_scope, vector_sig)   # 更新信号表

            # 不是信号和scope
            if (not (vector_sig or simple_sig or scope_begin or scope_end)):
                pass
                #print("Unsupported line: ", vcd_line)

    # 更新信号表
    def update_sig_tables(self, current_scope, signal_match):
        vcd_name = signal_match.group(1)                # vcd中信号代表字符名
        sig_name = signal_match.group(2)                # 信号名

        full_sig_name = current_scope + "." + sig_name  # 模块.信号名
        # print(full_sig_name)

        if full_sig_name in self.excluded_sigs:         # 该信号在排除范围内
            return
        
        # 将信号名与vcd文件中字符名，一一对应
        self.sig_name_2_vcd_name[full_sig_name] = vcd_name

        if vcd_name not in self.vcd_name_2_sig_name:
            self.vcd_name_2_sig_name[vcd_name] = []

        self.vcd_name_2_sig_name[vcd_name].append(full_sig_name)

    # 从vcd波形文件中提取信号值部分
    def extract_sig_values(self, vcd_file):
        for sig_name in self.sig_name_2_vcd_name.keys():    # 遍历信号名
            self.sigs_values[sig_name] = []                 # 信号值字典    键：信号名   值：列表（时间，信号值）

        # dumpvars_found = False

        while vcd_file: 
            vcd_line = vcd_file.readline().strip(' ')      # 读取一行
            if vcd_line == "":               # 注：如果是空行，为'\n'
                return
            elif vcd_line == "\n":
                continue

            # dumpvars = re.match(self.dumpvars_match, vcd_line)      # 匹配头
            new_time = re.match(self.new_time_match, vcd_line)      # 匹配时间
            sig_value = re.match(self.sig_value_match, vcd_line)    # 匹配信号值

            # if dumpvars:
            # dumpvars_found = True   # 找到dumpvars头,开始匹配信号值
            # current_time = 0        # 时间初始为0

            if new_time:
                current_time = new_time.group(1)        # 时间

            if current_time == '123018744':        # 时间
                pass
            if sig_value:
                signal_value = sig_value.group(1)       # 信号值（[zx10]+）
                signal_vcd_name = sig_value.group(2)    # 信号对应的vcd名
                if signal_vcd_name in self.vcd_name_2_sig_name:
                    # vcd名转信号名
                    signal_name_list = self.vcd_name_2_sig_name[signal_vcd_name]
                    for signal_name in signal_name_list:
                        # 信号值字典    键：信号名   值：列表（时间，信号值）
                        self.sigs_values[signal_name].append((int(current_time), signal_value))

                else:
                    # we currently get here for expended vector signals (i.e. [x[3]])
                    continue 


