from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type import HclType
from py_hcl.utils import auto_repr


@auto_repr(repr_fields=['hcl_type', 'conn_side'])
class Wire(HclExpr):
    def __init__(self, hcl_type: HclType):
        self.hcl_type = hcl_type
        self.conn_side = ConnSide.BOTH
