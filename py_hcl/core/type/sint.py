from py_hcl.core.type import HclType
from py_hcl.core.type.wrapper import bd_fld_wrap, vec_wrap
from py_hcl.utils import signed_num_bin_width
from py_hcl.core.type.error import TypeError
from py_hcl.core.expr.error import ExprError


@bd_fld_wrap
@vec_wrap
class SIntT(HclType):
    def __init__(self, width):
        if width <= 1:
            raise TypeError.size_err(
                f'SInt width can not equal or less than 1, got {width}')

        self.type = "sint"
        self.width = width

    def __call__(self, value: int):
        from py_hcl.core.expr.lit_sint import SLiteral

        least_len = signed_num_bin_width(value)
        if least_len > self.width:
            raise ExprError.out_of_range_err(
                f'Literal {value} out of range for sint[{self.width}]')

        u = SLiteral(value)
        u.hcl_type = SIntT(self.width)
        return u
