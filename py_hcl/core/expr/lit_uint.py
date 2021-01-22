from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import unsigned_num_bin_width


class ULiteral(HclExpr):
    def __init__(self, value: int):
        self.value = value

        w = unsigned_num_bin_width(value)
        self.hcl_type = UIntT(w)
        self.variable_type = VariableType.ReadOnly
