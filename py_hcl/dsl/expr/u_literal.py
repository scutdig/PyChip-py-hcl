from py_hcl.dsl.expr.hclexpr import HclExpr


class ULiteral(HclExpr):
    def __init__(self, value):
        self.value = value
