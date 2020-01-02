from py_hcl.core.type import HclType
from py_hcl.core.type.wrapper import bd_fld_wrap, vec_wrap
from py_hcl.utils import signed_num_bin_len


@bd_fld_wrap
@vec_wrap
class SIntT(HclType):
    def __init__(self, width):
        self.type = "sint"
        self.width = width

    def __call__(self, value: int):
        from py_hcl.core.expr.lit_sint import SLiteral

        # TODO: Accurate Error Message
        assert signed_num_bin_len(value) <= self.width
        u = SLiteral(value)
        u.hcl_type = SIntT(self.width)
        return u
