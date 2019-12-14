from py_hcl.core.expr import HclExpr


class ExprPlace(HclExpr):
    def __init__(self, hcl_type, assoc_value):
        self.hcl_type = hcl_type
        self.assoc_value = assoc_value
