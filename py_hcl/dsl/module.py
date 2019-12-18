from py_hcl.core import install_ops
from py_hcl.dsl.expr.io import IO
from ..core.module.meta_module import MetaModule

install_ops()


class Module(metaclass=MetaModule):
    io = IO()
