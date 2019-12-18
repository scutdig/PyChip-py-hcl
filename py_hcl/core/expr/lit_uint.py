from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import unsigned_num_bin_len


class ULiteral(HclExpr):
    def __init__(self, value: int):
        self.value = value

        w = unsigned_num_bin_len(value)
        self.hcl_type = UIntT(w)
        self.conn_side = ConnSide.RT
