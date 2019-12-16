from typing import Union

from multipledispatch import dispatch

from ...expr.prim_ops import Add, Sub, Mul, Div, Rem, \
    Lt, Leq, Gt, Geq, Eq, Neq, Xor, Or, And, Not, Neg, \
    Cat, Bits, AsUInt, AsSInt, Shl, Shr, Dshl, Dshr
from ...type import UIntType, SIntType, ClockType
from ...type_checker.utils import type_in, check_all_same_uint_sint

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Add)
def check(add: Add):
    from .. import check_all_expr
    if not check_all_expr(*add.args):
        return False

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
def check(sub: Sub):
    from .. import check_all_expr
    if not check_all_expr(*sub.args):
        return False

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
def check(mul: Mul):
    from .. import check_all_expr
    if not check_all_expr(*mul.args):
        return False

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
def check(div: Div):
    from .. import check_all_expr
    if not check_all_expr(*div.args):
        return False

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
def check(rem: Rem):
    from .. import check_all_expr
    if not check_all_expr(*rem.args):
        return False

    if not check_all_same_uint_sint(rem.args[0].tpe,
                                    rem.args[1].tpe,
                                    rem.tpe):
        return False

    expected_type_width = min(rem.args[0].tpe.width.width,
                              rem.args[1].tpe.width.width)
    if rem.tpe.width.width != expected_type_width:
        return False

    return True


@checker((Lt, Leq, Gt, Geq, Eq, Neq))
def check(comparison: Union[Lt, Leq, Gt, Geq, Eq, Neq]):
    from .. import check_all_expr
    if not check_all_expr(*comparison.args):
        return False

    if not check_all_same_uint_sint(comparison.args[0].tpe,
                                    comparison.args[1].tpe):
        return False

    if not type_in(comparison.tpe, UIntType):
        return False

    if comparison.tpe.width.width != 1:
        return False

    return True


@checker((And, Or, Xor))
def check(binary_bit: Union[And, Or, Xor]):
    from .. import check_all_expr
    if not check_all_expr(*binary_bit.args):
        return False

    if not check_all_same_uint_sint(binary_bit.args[0].tpe,
                                    binary_bit.args[1].tpe):
        return False

    if not type_in(binary_bit.tpe, UIntType):
        return False

    expected_type_width = max(binary_bit.args[0].tpe.width.width,
                              binary_bit.args[1].tpe.width.width)
    if binary_bit.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Not)
def check(n: Not):
    from .. import check_all_expr
    if not check_all_expr(n.arg):
        return False

    if not check_all_same_uint_sint(n.arg.tpe):
        return False

    if not type_in(n.tpe, UIntType):
        return False

    expected_type_width = n.arg.tpe.width.width
    if n.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Neg)
def check(neg: Neg):
    from .. import check_all_expr
    if not check_all_expr(neg.arg):
        return False

    if not check_all_same_uint_sint(neg.arg.tpe):
        return False

    if not type_in(neg.tpe, SIntType):
        return False

    expected_type_width = neg.arg.tpe.width.width + 1
    if neg.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Cat)
def check(cat: Cat):
    from .. import check_all_expr
    if not check_all_expr(*cat.args):
        return False

    if not check_all_same_uint_sint(cat.args[0].tpe,
                                    cat.args[1].tpe):
        return False

    if not type_in(cat.tpe, UIntType):
        return False

    expected_type_width = \
        cat.args[0].tpe.width.width + cat.args[1].tpe.width.width
    if cat.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Bits)
def check(bits: Bits):
    from .. import check_all_expr
    if not check_all_expr(bits.ir_arg):
        return False

    if not check_all_same_uint_sint(bits.ir_arg.tpe):
        return False

    if not type_in(bits.tpe, UIntType):
        return False

    if not \
            bits.ir_arg.tpe.width.width > \
            bits.const_args[0] >= \
            bits.const_args[1] >= 0:
        return False

    expected_type_width = bits.const_args[0] - bits.const_args[1] + 1
    if bits.tpe.width.width != expected_type_width:
        return False

    return True


@checker(AsUInt)
def check(as_uint: AsUInt):
    from .. import check_all_expr
    if not check_all_expr(as_uint.arg):
        return False

    if not type_in(as_uint.arg.tpe, UIntType, SIntType, ClockType):
        return False

    if not type_in(as_uint.tpe, UIntType):
        return False

    if type_in(as_uint.arg.tpe, ClockType):
        expected_type_width = 1
    else:
        expected_type_width = as_uint.arg.tpe.width.width

    if as_uint.tpe.width.width != expected_type_width:
        return False

    return True


@checker(AsSInt)
def check(as_sint: AsSInt):
    from .. import check_all_expr
    if not check_all_expr(as_sint.arg):
        return False

    if not type_in(as_sint.arg.tpe, UIntType, SIntType, ClockType):
        return False

    if not type_in(as_sint.tpe, SIntType):
        return False

    if type_in(as_sint.arg.tpe, ClockType):
        expected_type_width = 1
    else:
        expected_type_width = as_sint.arg.tpe.width.width

    if as_sint.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Shl)
def check(shl: Shl):
    from .. import check_all_expr
    if not check_all_expr(shl.ir_arg):
        return False

    if not check_all_same_uint_sint(shl.ir_arg.tpe, shl.tpe):
        return False

    expected_type_width = shl.ir_arg.tpe.width.width + shl.const_arg
    if shl.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Shr)
def check(shr: Shr):
    from .. import check_all_expr
    if not check_all_expr(shr.ir_arg):
        return False

    if not check_all_same_uint_sint(shr.ir_arg.tpe, shr.tpe):
        return False

    expected_type_width = shr.ir_arg.tpe.width.width - shr.const_arg
    expected_type_width = max(expected_type_width, 1)
    if shr.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Dshl)
def check(dshl: Dshl):
    from .. import check_all_expr
    if not check_all_expr(*dshl.args):
        return False

    if not check_all_same_uint_sint(dshl.args[0].tpe,
                                    dshl.tpe):
        return False

    if not type_in(dshl.args[1].tpe, UIntType):
        return False

    expected_type_width = \
        dshl.args[0].tpe.width.width + 2 ** dshl.args[1].tpe.width.width - 1
    if dshl.tpe.width.width != expected_type_width:
        return False

    return True


@checker(Dshr)
def check(dshr: Dshr):
    from .. import check_all_expr
    if not check_all_expr(*dshr.args):
        return False

    if not check_all_same_uint_sint(dshr.args[0].tpe,
                                    dshr.tpe):
        return False

    if not type_in(dshr.args[1].tpe, UIntType):
        return False

    expected_type_width = dshr.args[0].tpe.width.width
    if dshr.tpe.width.width != expected_type_width:
        return False

    return True
