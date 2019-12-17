from py_hcl.core import install_ops
from py_hcl.core.expr.mod_inst import con_module
from py_hcl.dsl.expr.io import IO, Input
from py_hcl.dsl.tpe.clock import Clock
from py_hcl.dsl.tpe.uint import Bool
from ..core.module.meta_module import MetaModule

install_ops()


class Module(metaclass=MetaModule):
    def __new__(cls):
        return con_module(cls)

    io = IO(
        clock=Input(Clock),
        reset=Input(Bool),
    )
