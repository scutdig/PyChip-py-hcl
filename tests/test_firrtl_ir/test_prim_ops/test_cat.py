from py_hcl.firrtl_ir.expr.prim_ops import Cat
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    cat = Cat(args, uw(9))
    assert check(cat)
    serialize_equal(cat, 'cat(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    cat = Cat(args, uw(10))
    assert check(cat)
    serialize_equal(cat, 'cat(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    cat = Cat(args, uw(12))
    assert check(cat)
    serialize_equal(cat, 'cat(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    cat = Cat(args, uw(11))
    assert check(cat)
    serialize_equal(cat, 'cat(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    cat = Cat(args, uw(11))
    assert check(cat)
    serialize_equal(cat, 'cat(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    cat = Cat(args, uw(12))
    assert check(cat)
    serialize_equal(cat, 'cat(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    cat = Cat(args, uw(6))
    assert not check(cat)

    args = [n("a", uw(6)), n("b", UnknownType())]
    cat = Cat(args, uw(6))
    assert not check(cat)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    cat = Cat(args, uw(14))
    assert not check(cat)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    cat = Cat(args, uw(26))
    assert not check(cat)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    cat = Cat(args, uw(6))
    assert not check(cat)

    args = [n("a", uw(6)), n("b", uw(6))]
    cat = Cat(args, uw(6))
    assert not check(cat)

    args = [n("b", sw(6)), n("a", sw(6))]
    cat = Cat(args, uw(11))
    assert not check(cat)

    args = [n("a", uw(6)), n("b", uw(6))]
    cat = Cat(args, uw(13))
    assert not check(cat)
