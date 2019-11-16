from py_hcl.firrtl_ir.expr.prim_ops import Mul
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    mul = Mul(args, uw(9))
    assert check(mul)
    serialize_equal(mul, 'mul(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    mul = Mul(args, uw(10))
    assert check(mul)
    serialize_equal(mul, 'mul(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    mul = Mul(args, uw(12))
    assert check(mul)
    serialize_equal(mul, 'mul(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    mul = Mul(args, sw(11))
    assert check(mul)
    serialize_equal(mul, 'mul(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    mul = Mul(args, sw(11))
    assert check(mul)
    serialize_equal(mul, 'mul(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    mul = Mul(args, sw(12))
    assert check(mul)
    serialize_equal(mul, 'mul(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    mul = Mul(args, sw(6))
    assert not check(mul)

    args = [n("a", uw(6)), n("b", UnknownType())]
    mul = Mul(args, uw(6))
    assert not check(mul)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    mul = Mul(args, sw(14))
    assert not check(mul)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    mul = Mul(args, uw(26))
    assert not check(mul)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    mul = Mul(args, sw(6))
    assert not check(mul)

    args = [n("a", uw(6)), n("b", uw(6))]
    mul = Mul(args, uw(6))
    assert not check(mul)

    args = [n("b", sw(6)), n("a", sw(6))]
    mul = Mul(args, sw(11))
    assert not check(mul)

    args = [n("a", uw(6)), n("b", uw(6))]
    mul = Mul(args, uw(13))
    assert not check(mul)
