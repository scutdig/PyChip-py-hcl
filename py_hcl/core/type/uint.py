from py_hcl.core.expr.error import ExprError
from py_hcl.core.type import HclType
from py_hcl.core.type.wrapper import bd_fld_wrap, vec_wrap
from py_hcl.utils import unsigned_num_bin_width
from py_hcl.core.type.error import TypeError


@bd_fld_wrap
@vec_wrap
class UIntT(HclType):
    def __init__(self, width):
        if width <= 0:
            raise TypeError.size_err(
                f'UInt width can not equal or less than 0, got {width}')

        self.type = "uint"
        self.width = width

    def __call__(self, value: int):
        from py_hcl.core.expr.lit_uint import ULiteral

        least_len = unsigned_num_bin_width(value)
        if least_len > self.width:
            raise ExprError.out_of_range_err(
                f'Literal {value} out of range for uint[{self.width}]')

        u = ULiteral(value)
        u.hcl_type = UIntT(self.width)
        return u
