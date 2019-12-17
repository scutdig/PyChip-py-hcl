from py_hcl.core.type import HclType
from py_hcl.utils import unsigned_num_bin_len


class UIntT(HclType):
    def __init__(self, width):
        self.width = width

    def __call__(self, value: int):
        from py_hcl.core.expr.lit_uint import ULiteral

        assert unsigned_num_bin_len(value) <= self.width
        u = ULiteral(value)
        u.hcl_type = UIntT(self.width)
        return u
