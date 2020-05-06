import os
from collections import Counter
from typing import Dict

from pyhcl.core._dynamic_ctx import DynamicContext
from pyhcl.core._emit_context import EmitterContext
from pyhcl.dsl.module import Module
from pyhcl.ir import low_ir


class Emitter:
    @staticmethod
    def emit(m: Module) -> str:
        circuit = Emitter.elaborate(m)
        return circuit.serialize()

    @staticmethod
    def elaborate(m: Module) -> low_ir.Circuit:
        ec: EmitterContext = EmitterContext(m, {}, Counter())
        modIRs: Dict[int, low_ir.DefModule] = ec.emit()
        circuit = low_ir.Circuit(list(modIRs.values()), ec.name)
        DynamicContext.clearScope()
        return circuit

    @staticmethod
    def dump(s, filename) -> str:
        if not os.path.exists('.fir'):
            os.mkdir('.fir')

        f = os.path.join('.fir', filename)
        with open(f, "w+") as fir_file:
            fir_file.write(s)

        return f

    @staticmethod
    def dumpVerilog(filename):
        os.system('firrtl -i %s -o %s -X verilog' % (filename, filename))