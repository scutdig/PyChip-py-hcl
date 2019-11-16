from py_hcl.firrtl_ir.expr.prim_ops import Div
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    div = Div(args, uw(5))
    assert check(div)
    serialize_equal(div, 'div(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    div = Div(args, uw(6))
    assert check(div)
    serialize_equal(div, 'div(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    div = Div(args, uw(6))
    assert check(div)
    serialize_equal(div, 'div(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    div = Div(args, sw(7))
    assert check(div)
    serialize_equal(div, 'div(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    div = Div(args, sw(7))
    assert check(div)
    serialize_equal(div, 'div(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    div = Div(args, sw(7))
    assert check(div)
    serialize_equal(div, 'div(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    div = Div(args, sw(7))
    assert not check(div)

    args = [n("a", uw(6)), n("b", UnknownType())]
    div = Div(args, uw(6))
    assert not check(div)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    div = Div(args, sw(11))
    assert not check(div)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    div = Div(args, uw(6))
    assert not check(div)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    div = Div(args, sw(6))
    assert not check(div)

    args = [n("a", uw(6)), n("b", uw(6))]
    div = Div(args, uw(7))
    assert not check(div)

    args = [n("b", sw(6)), n("a", sw(6))]
    div = Div(args, sw(1))
    assert not check(div)

    args = [n("a", uw(6)), n("b", uw(6))]
    div = Div(args, uw(13))
    assert not check(div)
