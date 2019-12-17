from py_hcl.core.type import HclType
from py_hcl.utils import signed_num_bin_len


class SIntT(HclType):
    def __init__(self, width):
        self.width = width

    def __call__(self, value: int):
        from py_hcl.core.expr.lit_sint import SLiteral

        assert signed_num_bin_len(value) <= self.width
        u = SLiteral(value)
        u.hcl_type = SIntT(self.width)
        return u
