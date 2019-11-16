from py_hcl.firrtl_ir.expr.prim_ops import Eq
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    eq = Eq(args, uw(1))
    assert check(eq)
    serialize_equal(eq, 'eq(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    eq = Eq(args, uw(1))
    assert check(eq)
    serialize_equal(eq, 'eq(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    eq = Eq(args, uw(1))
    assert check(eq)
    serialize_equal(eq, 'eq(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    eq = Eq(args, uw(1))
    assert check(eq)
    serialize_equal(eq, 'eq(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    eq = Eq(args, uw(1))
    assert check(eq)
    serialize_equal(eq, 'eq(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    eq = Eq(args, uw(1))
    assert check(eq)
    serialize_equal(eq, 'eq(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    eq = Eq(args, uw(1))
    assert not check(eq)

    args = [n("a", uw(6)), n("b", UnknownType())]
    eq = Eq(args, uw(1))
    assert not check(eq)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    eq = Eq(args, uw(1))
    assert not check(eq)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    eq = Eq(args, uw(1))
    assert not check(eq)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    eq = Eq(args, uw(6))
    assert not check(eq)

    args = [n("a", uw(6)), n("b", uw(6))]
    eq = Eq(args, uw(6))
    assert not check(eq)

    args = [n("b", sw(6)), n("a", sw(6))]
    eq = Eq(args, uw(0))
    assert not check(eq)

    args = [n("a", uw(6)), n("b", uw(6))]
    eq = Eq(args, uw(10))
    assert not check(eq)
