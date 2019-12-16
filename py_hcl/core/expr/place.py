from py_hcl.core.expr import HclExpr, ConnDir
from py_hcl.core.type import HclType


class ExprPlace(HclExpr):
    def __init__(self, hcl_type: HclType, assoc_value, conn_dir: ConnDir):
        super().__init__()
        self.hcl_type = hcl_type
        self.assoc_value = assoc_value
        self.conn_dir = conn_dir
