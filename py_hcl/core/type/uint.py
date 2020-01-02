from py_hcl.core.type import HclType
from py_hcl.core.type.wrapper import bd_fld_wrap, vec_wrap
from py_hcl.utils import unsigned_num_bin_len


@bd_fld_wrap
@vec_wrap
class UIntT(HclType):
    def __init__(self, width):
        self.type = "uint"
        self.width = width

    def __call__(self, value: int):
        from py_hcl.core.expr.lit_uint import ULiteral

        # TODO: Accurate Error Message
        assert unsigned_num_bin_len(value) <= self.width
        u = ULiteral(value)
        u.hcl_type = UIntT(self.width)
        return u
