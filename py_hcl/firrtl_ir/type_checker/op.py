from .utils import type_in, check_all_same_uint_sint
from ..type import UIntType, SIntType, ClockType
from ..expr.prim_ops import Add, Sub, Mul, Div, Rem, \
    Lt, Leq, Gt, Geq, Eq, Neq, Xor, Or, And, Not, Neg, \
    Cat, Bits, AsUInt, AsSInt, Shl, Shr, Dshl, Dshr


class OpTypeChecker(object):
    op_checker_map = {}

    @staticmethod
    def check(op_obj):
        try:
            return OpTypeChecker.op_checker_map[type(op_obj)](op_obj)
        except KeyError:
            raise NotImplementedError(type(op_obj))


def checker(*op):
    def f(func):
        for o in op:
            OpTypeChecker.op_checker_map[o] = func
        return func

    return f


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Add)
def _(add):
    if not check_all_same_uint_sint(add.args[0].tpe,
                                    add.args[1].tpe,
                                    add.tpe):
        return False

    expected_type_width = max(add.args[0].tpe.width.width,
                              add.args[1].tpe.width.width) + 1
    if add.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Sub)
def _(sub):
    if not check_all_same_uint_sint(sub.args[0].tpe,
                                    sub.args[1].tpe):
        return False

    if not type_in(sub.tpe, SIntType):
        return False

    expected_type_width = max(sub.args[0].tpe.width.width,
                              sub.args[1].tpe.width.width) + 1
    if sub.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Mul)
def _(mul):
    if not check_all_same_uint_sint(mul.args[0].tpe,
                                    mul.args[1].tpe,
                                    mul.tpe):
        return False

    expected_type_width = \
        mul.args[0].tpe.width.width + mul.args[1].tpe.width.width
    if mul.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Div)
def _(div):
    if not check_all_same_uint_sint(div.args[0].tpe,
                                    div.args[1].tpe,
                                    div.tpe):
        return False

    expected_type_width = div.args[0].tpe.width.width
    if type_in(div.args[0].tpe, SIntType):
        expected_type_width += 1
    if div.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Rem)
def _(rem):
    if not check_all_same_uint_sint(rem.args[0].tpe,
                                    rem.args[1].tpe,
                                    rem.tpe):
        return False

    expected_type_width = min(rem.args[0].tpe.width.width,
                              rem.args[1].tpe.width.width)
    if rem.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Lt, Leq, Gt, Geq, Eq, Neq)
def _(comparison):
    if not check_all_same_uint_sint(comparison.args[0].tpe,
                                    comparison.args[1].tpe):
        return False

    if not type_in(comparison.tpe, UIntType):
        return False

    if comparison.tpe.width.width != 1:
        return False

    return True


@checker(And, Or, Xor)
def _(binary_bit):
    if not check_all_same_uint_sint(binary_bit.args[0].tpe,
                                    binary_bit.args[1].tpe,
                                    binary_bit.tpe):
        return False

    expected_type_width = max(binary_bit.args[0].tpe.width.width,
                              binary_bit.args[1].tpe.width.width)
    if binary_bit.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Not)
def _(n):
    if not check_all_same_uint_sint(n.arg.tpe,
                                    n.tpe):
        return False

    expected_type_width = n.arg.tpe.width.width
    if n.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Neg)
def _(neg):
    if not check_all_same_uint_sint(neg.arg.tpe,
                                    neg.tpe):
        return False

    expected_type_width = neg.arg.tpe.width.width + 1
    if neg.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Cat)
def _(cat):
    if not check_all_same_uint_sint(cat.args[0].tpe,
                                    cat.args[1].tpe,
                                    cat.tpe):
        return False

    expected_type_width = \
        cat.args[0].tpe.width.width + cat.args[1].tpe.width.width
    if cat.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Bits)
def _(bits):
    if not check_all_same_uint_sint(bits.ir_arg.tpe):
        return False

    if not type_in(bits.tpe, UIntType):
        return False

    if not \
            bits.tpe.width.width >= \
            bits.const_args[0] >= \
            bits.const_args[1] >= 0:
        return False

    expected_type_width = bits.const_args[0] - bits.const_args[1] + 1
    if bits.tpe.width.width != expected_type_width:
        return False

    return True


@checker(AsUInt)
def _(as_uint):
    if not type_in(as_uint.arg.tpe, UIntType, SIntType, ClockType):
        return False

    if not type_in(as_uint.tpe, UIntType):
        return False

    expected_type_width = as_uint.arg.width.width
    if type_in(as_uint.tpe, ClockType):
        expected_type_width = 1
    if as_uint.tpe.width.width != expected_type_width:
        return False

    return True


@checker(AsSInt)
def _(as_sint):
    if not type_in(as_sint.arg.tpe, UIntType, SIntType, ClockType):
        return False

    if not type_in(as_sint.tpe, SIntType):
        return False

    expected_type_width = as_sint.arg.width.width
    if type_in(as_sint.tpe, ClockType):
        expected_type_width = 1
    if as_sint.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Shl)
def _(shl):
    if not check_all_same_uint_sint(shl.ir_arg.tpe, shl.tpe):
        return False

    expected_type_width = shl.ir_arg.width.width + shl.const_arg
    if shl.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Shr)
def _(shr):
    if not check_all_same_uint_sint(shr.ir_arg.tpe, shr.tpe):
        return False

    expected_type_width = shr.ir_arg.width.width - shr.const_arg
    expected_type_width = max(expected_type_width, 1)
    if shr.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Dshl)
def _(dshl):
    if not check_all_same_uint_sint(dshl.args[0].tpe,
                                    dshl.tpe):
        return False

    if type_in(dshl.args[1].tpe, UIntType):
        return False

    expected_type_width = \
        dshl.args[0].width.width + 2 ** dshl.args[1].width.width - 1
    if dshl.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Dshr)
def _(dshr):
    if not check_all_same_uint_sint(dshr.args[0].tpe,
                                    dshr.tpe):
        return False

    if type_in(dshr.args[1].tpe, UIntType):
        return False

    expected_type_width = dshr.args[0].width.width
    if dshr.tpe.width.width != expected_type_width:
        return False

    return True
