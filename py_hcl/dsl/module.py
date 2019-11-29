from py_hcl.dsl.expr.io import IO
from ..core.module_constructor.meta_module import MetaModule
from py_hcl.dsl.expr.expression import Expression


class Module(metaclass=MetaModule):
    io = IO()  # TODO
    clock = Expression()  # TODO
    reset = Expression()  # TODO
