from py_hcl.core.expr import ExprHolder
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.utils import auto_repr


@auto_repr(repr_fields=['module_name'])
class ModuleInst(object):
    def __init__(self, module_cls):
        self.packed_module = module_cls.packed_module
        self.module_name = module_cls.packed_module.name


def con_module(module_cls):
    return ExprHolder(module_cls.io.hcl_type.rev(),
                      ConnSide.BOTH, ModuleInst(module_cls))
