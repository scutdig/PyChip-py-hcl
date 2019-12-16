from py_hcl.core.expr import HclExpr, ConnDir
from py_hcl.core.type import HclType


class Wire(HclExpr):
    def __init__(self, hcl_type: HclType):
        super().__init__()
        self.hcl_type = hcl_type
        self.conn_dir = ConnDir.BOTH
