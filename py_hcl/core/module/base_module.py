from py_hcl.core import install_ops
from py_hcl.core.expr.io import io_extend
from py_hcl.core.module.meta_module import MetaModule

install_ops()


class BaseModule(metaclass=MetaModule):
    io = io_extend(tuple())({})
