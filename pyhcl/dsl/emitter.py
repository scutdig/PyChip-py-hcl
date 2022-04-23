import os
from collections import Counter
from typing import Dict

from pyhcl.core._dynamic_ctx import DynamicContext
from pyhcl.core._emit_context import EmitterContext
from pyhcl.dsl.module import Module
from pyhcl.ir import low_ir
from pyhcl.util.firrtltools import replacewithfirmod
from pyhcl.dsl.stage import Form, HighForm


class Emitter:
    @staticmethod
    def elaborate(m: Module) -> low_ir.Circuit:
        ec: EmitterContext = EmitterContext(m, {}, Counter())
        modIRs: Dict[int, low_ir.DefModule] = ec.emit()
        modIRs = replacewithfirmod(modIRs)
        circuit = low_ir.Circuit(list(modIRs.values()), ec.name)
        DynamicContext.clearScope()
        return circuit

    @staticmethod
    def emit(m: Module, f: Form = HighForm) -> str:
        return f(Emitter.elaborate(m)).emit()

    @staticmethod
    def dump(s, filename) -> str:
        if not os.path.exists('.fir'):
            os.mkdir('.fir')

        f = os.path.join('.fir', filename)
        with open(f, "w+") as fir_file:
            fir_file.write(s)

        return f

    @staticmethod
    def dumpVerilog(filename, use_jar=False):
        if use_jar:
            os.system('java -jar firrtl.jar -i %s -o %s -X verilog' % (filename, filename))
        else:
            os.system('firrtl -i %s -o %s -X verilog' % (filename, filename))
    
    @staticmethod
    def dumpMidForm(filename, use_jar=False):
        if use_jar:
            os.system('java -jar firrtl.jar -i %s -o %s -X middle' % (filename, filename))
        else:
            os.system('firrtl -i %s -o %s -X middle' % (filename, filename))
    
    @staticmethod
    def dumpLoweredForm(filename, use_jar):
        if use_jar:
            os.system('java -jar firrtl.jar -i %s -o %s -X low' % (filename, filename))
        else:
            os.system('firrtl -i %s -o %s -X low' % (filename, filename))
