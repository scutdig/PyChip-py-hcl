from abc import ABC, abstractclassmethod
from dataclasses import dataclass

from pyhcl.ir import low_ir
from pyhcl.dsl.check_and_infer import CheckAndInfer
from pyhcl.passes.replace_subaccess import ReplaceSubaccess
from pyhcl.passes.replace_subindex import ReplaceSubindex
from pyhcl.passes.expand_aggregate import ExpandAggregate

class Form(ABC):
    @abstractclassmethod
    def emit(self) -> str:
        ...

@dataclass
class HighForm(Form):
    c: low_ir.Circuit

    def emit(self) -> str:
        self.c = CheckAndInfer.run(self.c)
        return self.c.serialize()

@dataclass
class MidForm(Form):
    def emit(self) -> str:
        ...

@dataclass
class LowForm(Form):
    c: low_ir.Circuit

    def emit(self) -> str:
        self.c = CheckAndInfer.run(self.c)
        self.c = ReplaceSubaccess().run(self.c)
        self.c = ReplaceSubindex().run(self.c)
        self.c = ExpandAggregate().run(self.c)
        return self.c.serialize()

@dataclass
class Verilog(Form):
    c: low_ir.Circuit

    def emit(self) -> str:
        self.c = CheckAndInfer.run(self.c)
        self.c = ReplaceSubaccess().run(self.c)
        self.c = ReplaceSubindex().run(self.c)
        self.c = ExpandAggregate().run(self.c)
        return self.c.verilog_serialize()