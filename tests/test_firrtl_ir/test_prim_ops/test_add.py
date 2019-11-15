from py_hcl.firrtl_ir.expr.prim_ops import Add
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.tpe import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    add = Add(args, uw(6))
    assert check(add)
    serialize_equal(add, 'add(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    add = Add(args, uw(7))
    assert check(add)
    serialize_equal(add, 'add(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    add = Add(args, uw(7))
    assert check(add)
    serialize_equal(add, 'add(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    add = Add(args, sw(7))
    assert check(add)
    serialize_equal(add, 'add(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    add = Add(args, sw(7))
    assert check(add)
    serialize_equal(add, 'add(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    add = Add(args, sw(7))
    assert check(add)
    serialize_equal(add, 'add(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    add = Add(args, sw(7))
    assert not check(add)

    args = [n("a", uw(6)), n("b", UnknownType())]
    add = Add(args, sw(7))
    assert not check(add)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    add = Add(args, sw(7))
    assert not check(add)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    add = Add(args, sw(7))
    assert not check(add)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    add = Add(args, sw(6))
    assert not check(add)

    args = [n("a", uw(6)), n("b", uw(6))]
    add = Add(args, uw(6))
    assert not check(add)

    args = [n("b", sw(6)), n("a", sw(6))]
    add = Add(args, sw(1))
    assert not check(add)

    args = [n("a", uw(6)), n("b", uw(6))]
    add = Add(args, uw(10))
    assert not check(add)
