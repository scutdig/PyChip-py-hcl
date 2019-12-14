from py_hcl.core.hcl_ops import op_map
from py_hcl.core.type import HclType


class HclExpr(object):
    def __init__(self):
        self.hcl_type = HclType()

    def __ilshift__(self, other):
        return op_map['<<='](self, other)

    def __add__(self, other):
        return op_map['+'](self, other)

    def __getattr__(self, item):
        return op_map['.'](self, item)
