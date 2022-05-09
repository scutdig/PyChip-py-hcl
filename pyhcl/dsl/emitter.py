import os
from collections import Counter
from typing import Dict

from pyhcl.core._dynamic_ctx import DynamicContext
from pyhcl.core._emit_context import EmitterContext
from pyhcl.dsl.module import Module
from pyhcl.ir import low_ir
from pyhcl.util.firrtltools import replacewithfirmod


class Emitter:
    # 传入模块对象，返回str---firrtl代码
    @staticmethod
    def emit(m: Module, toverilog=False) -> str:
        circuit = Emitter.elaborate(m)
        # 将Circuit对象转化为str
        if(toverilog):
            return circuit.verilog_serialize()
        else:
            return circuit.serialize()      # firrtl代码

    # 传入模块对象，返回Circuit对象
    @staticmethod
    def elaborate(m: Module) -> low_ir.Circuit:
        ec: EmitterContext = EmitterContext(m, {}, Counter())
        modIRs: Dict[int, low_ir.DefModule] = ec.emit()
        modIRs = replacewithfirmod(modIRs)
        circuit = low_ir.Circuit(list(modIRs.values()), ec.name)
        DynamicContext.clearScope()
        return circuit

    # 传入firrtl代码和文件名，将firrtl代码写入文件中，并返回文件路径
    @staticmethod
    def dump(s, filename) -> str:
        if not os.path.exists('.fir'):
            os.mkdir('.fir')

        f = os.path.join('.fir', filename)
        with open(f, "w+") as fir_file:
            fir_file.write(s)

        return f

    # 传入firrtl文件路径，执行firrtl命令，将firrtl代码编译为verilog代码
    @staticmethod
    def dumpVerilog(filename):
        os.system('firrtl -i %s -o %s -X verilog' % (filename, filename))