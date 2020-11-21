from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type import HclType
from py_hcl.utils import json_serialize


@json_serialize(json_fields=['hcl_type', 'variable_type'])
class Wire(HclExpr):
    def __init__(self, hcl_type: HclType):
        self.hcl_type = hcl_type
        self.variable_type = VariableType.ASSIGNABLE_VALUE
