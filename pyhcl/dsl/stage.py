from abc import ABC, abstractclassmethod
from dataclasses import dataclass

from pyhcl.ir import low_ir
from pyhcl.passes.check_form import CheckHighForm
from pyhcl.passes.check_types import CheckTypes
from pyhcl.passes.check_flows import CheckFlow
from pyhcl.passes.check_widths import CheckWidths
from pyhcl.passes.auto_inferring import AutoInferring
from pyhcl.passes.replace_subaccess import ReplaceSubaccess
from pyhcl.passes.expand_aggregate import ExpandAggregate
from pyhcl.passes.expand_whens import ExpandWhens
from pyhcl.passes.expand_memory import ExpandMemory
from pyhcl.passes.optimize import Optimize
from pyhcl.passes.verilog_optimize import VerilogOptimize
from pyhcl.passes.remove_access import RemoveAccess
from pyhcl.passes.expand_sequential import ExpandSequential
from pyhcl.passes.handle_instance import HandleInstance
from pyhcl.passes.utils import AutoName

class Form(ABC):
    @abstractclassmethod
    def emit(self) -> str:
        ...

@dataclass
class HighForm(Form):
    c: low_ir.Circuit

    def emit(self) -> str:
        self.c = CheckHighForm(self.c).run()
        self.c = AutoInferring().run(self.c)
        self.c = CheckTypes().run(self.c)
        self.c = CheckFlow().run(self.c)
        self.c = CheckWidths().run(self.c)
        return self.c.serialize()

@dataclass
class MidForm(Form):
    def emit(self) -> str:
        ...

@dataclass
class LowForm(Form):
    c: low_ir.Circuit

    def emit(self) -> str:
        AutoName()
        self.c = CheckHighForm(self.c).run()
        self.c = AutoInferring().run(self.c)
        self.c = CheckTypes().run(self.c)
        self.c = CheckFlow().run(self.c)
        self.c = CheckWidths().run(self.c)
        self.c = ExpandMemory().run(self.c)
        self.c = ReplaceSubaccess().run(self.c)
        self.c = ExpandAggregate().run(self.c)
        self.c = RemoveAccess().run(self.c)
        self.c = ExpandWhens().run(self.c)
        self.c = HandleInstance().run(self.c)
        self.c = Optimize().run(self.c)
        return self.c.serialize()

@dataclass
class Verilog(Form):
    c: low_ir.Circuit

    def emit(self) -> str:
        AutoName()
        self.c = CheckHighForm(self.c).run()
        self.c = AutoInferring().run(self.c)
        self.c = CheckTypes().run(self.c)
        self.c = CheckFlow().run(self.c)
        self.c = CheckWidths().run(self.c)
        self.c = ExpandAggregate().run(self.c)
        self.c = ReplaceSubaccess().run(self.c)
        self.c = RemoveAccess().run(self.c)
        self.c = VerilogOptimize().run(self.c)
        self.c = ExpandSequential().run(self.c)
        self.c = HandleInstance().run(self.c)
        self.c = Optimize().run(self.c)
        return self.c.verilog_serialize()