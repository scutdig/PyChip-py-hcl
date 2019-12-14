from py_hcl.core.expr import HclExpr


class ULiteral(HclExpr):
    def __init__(self, value):
        self.value = value
