from py_hcl.firrtl_ir.expr.prim_ops import Rem
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    rem = Rem(args, uw(4))
    assert check(rem)
    serialize_equal(rem, 'rem(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    rem = Rem(args, uw(4))
    assert check(rem)
    serialize_equal(rem, 'rem(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    rem = Rem(args, uw(6))
    assert check(rem)
    serialize_equal(rem, 'rem(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    rem = Rem(args, sw(5))
    assert check(rem)
    serialize_equal(rem, 'rem(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    rem = Rem(args, sw(5))
    assert check(rem)
    serialize_equal(rem, 'rem(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    rem = Rem(args, sw(6))
    assert check(rem)
    serialize_equal(rem, 'rem(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    rem = Rem(args, sw(6))
    assert not check(rem)

    args = [n("a", uw(6)), n("b", UnknownType())]
    rem = Rem(args, uw(6))
    assert not check(rem)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    rem = Rem(args, sw(6))
    assert not check(rem)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    rem = Rem(args, uw(6))
    assert not check(rem)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    rem = Rem(args, sw(7))
    assert not check(rem)

    args = [n("a", uw(6)), n("b", uw(6))]
    rem = Rem(args, uw(7))
    assert not check(rem)

    args = [n("b", sw(6)), n("a", sw(6))]
    rem = Rem(args, sw(1))
    assert not check(rem)

    args = [n("a", uw(6)), n("b", uw(6))]
    rem = Rem(args, uw(10))
    assert not check(rem)
