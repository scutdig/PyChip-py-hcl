from py_hcl.firrtl_ir.expr.prim_ops import And
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check, OpTypeChecker
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    simple_and = And(args, uw(5))
    assert OpTypeChecker.check(simple_and)
    assert check(simple_and)
    serialize_equal(simple_and, 'and(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    simple_and = And(args, uw(6))
    assert OpTypeChecker.check(simple_and)
    assert check(simple_and)
    serialize_equal(simple_and, 'and(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    simple_and = And(args, uw(6))
    assert OpTypeChecker.check(simple_and)
    assert check(simple_and)
    serialize_equal(simple_and, 'and(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    simple_and = And(args, uw(6))
    assert OpTypeChecker.check(simple_and)
    assert check(simple_and)
    serialize_equal(simple_and, 'and(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    simple_and = And(args, uw(6))
    assert OpTypeChecker.check(simple_and)
    assert check(simple_and)
    serialize_equal(simple_and, 'and(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    simple_and = And(args, uw(6))
    assert OpTypeChecker.check(simple_and)
    assert check(simple_and)
    serialize_equal(simple_and, 'and(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    simple_and = And(args, uw(6))
    assert not OpTypeChecker.check(simple_and)
    assert not check(simple_and)

    args = [n("a", uw(6)), n("b", UnknownType())]
    simple_and = And(args, uw(6))
    assert not OpTypeChecker.check(simple_and)
    assert not check(simple_and)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    simple_and = And(args, uw(8))
    assert not OpTypeChecker.check(simple_and)
    assert not check(simple_and)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    simple_and = And(args, uw(20))
    assert not OpTypeChecker.check(simple_and)
    assert not check(simple_and)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    simple_and = And(args, uw(7))
    assert not OpTypeChecker.check(simple_and)
    assert not check(simple_and)

    args = [n("a", uw(6)), n("b", uw(6))]
    simple_and = And(args, uw(7))
    assert not OpTypeChecker.check(simple_and)
    assert not check(simple_and)

    args = [n("b", sw(6)), n("a", sw(6))]
    simple_and = And(args, uw(1))
    assert not OpTypeChecker.check(simple_and)
    assert not check(simple_and)

    args = [n("a", uw(6)), n("b", uw(6))]
    simple_and = And(args, uw(10))
    assert not OpTypeChecker.check(simple_and)
    assert not check(simple_and)
