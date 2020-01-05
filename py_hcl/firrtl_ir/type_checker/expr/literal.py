import logging

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
        logging.error("uint: type check failed - {}".format(uint.tpe))
        return False

    if uint.value < 0:
        logging.error("uint: value check failed - {}".format(uint.value))
        return False

    if unsigned_num_bin_len(uint.value) > uint.tpe.width.width:
        logging.error("uint: width check failed - {} > {}".format(
            unsigned_num_bin_len(uint.value), uint.tpe.width.width)
        )
        return False

    return True


@checker(SIntLiteral)
def check(sint: SIntLiteral):
    if not type_in(sint.tpe, SIntType):
        logging.error("sint: type check failed - {}".format(sint.tpe))
        return False

    if signed_num_bin_len(sint.value) > sint.tpe.width.width:
        logging.error("sint: width check failed - {} > {}".format(
            signed_num_bin_len(sint.value), sint.tpe.width.width)
        )
        return False

    return True
