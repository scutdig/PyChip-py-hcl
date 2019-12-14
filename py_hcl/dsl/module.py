from py_hcl.core import install_ops
from py_hcl.dsl.expr.io import IO, Input
from py_hcl.dsl.tpe.clock import Clock
from py_hcl.dsl.tpe.uint import Bool
from ..core.module.meta_module import MetaModule

install_ops()


class Module(metaclass=MetaModule):
    io = IO(
        clock=Input(Clock),
        reset=Input(Bool),
    )
