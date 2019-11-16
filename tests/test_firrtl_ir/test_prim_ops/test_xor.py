from py_hcl.firrtl_ir.expr.prim_ops import Xor
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    simple_xor = Xor(args, uw(5))
    assert check(simple_xor)
    serialize_equal(simple_xor, 'xor(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    simple_xor = Xor(args, uw(6))
    assert check(simple_xor)
    serialize_equal(simple_xor, 'xor(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    simple_xor = Xor(args, uw(6))
    assert check(simple_xor)
    serialize_equal(simple_xor, 'xor(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    simple_xor = Xor(args, uw(6))
    assert check(simple_xor)
    serialize_equal(simple_xor, 'xor(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    simple_xor = Xor(args, uw(6))
    assert check(simple_xor)
    serialize_equal(simple_xor, 'xor(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    simple_xor = Xor(args, uw(6))
    assert check(simple_xor)
    serialize_equal(simple_xor, 'xor(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    simple_xor = Xor(args, uw(6))
    assert not check(simple_xor)

    args = [n("a", uw(6)), n("b", UnknownType())]
    simple_xor = Xor(args, uw(6))
    assert not check(simple_xor)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    simple_xor = Xor(args, uw(8))
    assert not check(simple_xor)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    simple_xor = Xor(args, uw(20))
    assert not check(simple_xor)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    simple_xor = Xor(args, uw(7))
    assert not check(simple_xor)

    args = [n("a", uw(6)), n("b", uw(6))]
    simple_xor = Xor(args, uw(7))
    assert not check(simple_xor)

    args = [n("b", sw(6)), n("a", sw(6))]
    simple_xor = Xor(args, uw(1))
    assert not check(simple_xor)

    args = [n("a", uw(6)), n("b", uw(6))]
    simple_xor = Xor(args, uw(10))
    assert not check(simple_xor)
