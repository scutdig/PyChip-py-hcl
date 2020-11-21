from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.connect import VariableType
from py_hcl.utils import json_serialize


@json_serialize(
    json_fields=['id', 'type', 'hcl_type', "variable_type", 'module_name'])
class ModuleInst(HclExpr):
    def __init__(self, module_cls):
        self.type = 'module_inst'
        self.hcl_type = module_cls.io.hcl_type
        self.variable_type = VariableType.LOCATION
        self.packed_module = module_cls.packed_module
        self.module_name = module_cls.packed_module.name


def con_module(module_cls):
    return ModuleInst(module_cls)
