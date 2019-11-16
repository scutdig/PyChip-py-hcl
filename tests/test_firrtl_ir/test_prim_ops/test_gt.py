from py_hcl.firrtl_ir.expr.prim_ops import Gt
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    gt = Gt(args, uw(1))
    assert check(gt)
    serialize_equal(gt, 'gt(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    gt = Gt(args, uw(1))
    assert check(gt)
    serialize_equal(gt, 'gt(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    gt = Gt(args, uw(1))
    assert check(gt)
    serialize_equal(gt, 'gt(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    gt = Gt(args, uw(1))
    assert check(gt)
    serialize_equal(gt, 'gt(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    gt = Gt(args, uw(1))
    assert check(gt)
    serialize_equal(gt, 'gt(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    gt = Gt(args, uw(1))
    assert check(gt)
    serialize_equal(gt, 'gt(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    gt = Gt(args, uw(1))
    assert not check(gt)

    args = [n("a", uw(6)), n("b", UnknownType())]
    gt = Gt(args, uw(1))
    assert not check(gt)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    gt = Gt(args, uw(1))
    assert not check(gt)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    gt = Gt(args, uw(1))
    assert not check(gt)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    gt = Gt(args, uw(6))
    assert not check(gt)

    args = [n("a", uw(6)), n("b", uw(6))]
    gt = Gt(args, uw(6))
    assert not check(gt)

    args = [n("b", sw(6)), n("a", sw(6))]
    gt = Gt(args, uw(0))
    assert not check(gt)

    args = [n("a", uw(6)), n("b", uw(6))]
    gt = Gt(args, uw(10))
    assert not check(gt)
