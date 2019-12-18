from py_hcl.core.expr import HclExpr
from py_hcl.core.type.vector import VectorT


class VecHolder(HclExpr):
    def __init__(self, hcl_type, conn_side, assoc_value):
        self.hcl_type = hcl_type
        self.conn_side = conn_side

        assert isinstance(hcl_type, VectorT)
        assert hcl_type.size == len(assoc_value)
        self.assoc_value = assoc_value
