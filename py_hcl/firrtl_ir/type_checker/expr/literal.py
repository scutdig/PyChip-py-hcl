from multipledispatch import dispatch

from ..utils import type_in
from ...expr.literal import SIntLiteral, SIntType, UIntLiteral, UIntType
from py_hcl.utils import signed_num_bin_len, unsigned_num_bin_len

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(UIntLiteral)
def check(uint: UIntLiteral):
    if not type_in(uint.tpe, UIntType):
        return False

    if uint.value < 0:
        return False

    if unsigned_num_bin_len(uint.value) > uint.tpe.width.width:
        return False

    return True


@checker(SIntLiteral)
def check(sint: SIntLiteral):
    if not type_in(sint.tpe, SIntType):
        return False

    if signed_num_bin_len(sint.value) > sint.tpe.width.width:
        return False

    return True
