from py_hcl.firrtl_ir.expr.prim_ops import Neg
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    arg = u(20, w(5))
    neg = Neg(arg, sw(6))
    assert check(neg)
    serialize_equal(neg, 'neg(UInt<5>("14"))')

    arg = n("a", uw(6))
    neg = Neg(arg, sw(7))
    assert check(neg)
    serialize_equal(neg, 'neg(a)')

    arg = s(20, w(6))
    neg = Neg(arg, sw(7))
    assert check(neg)
    serialize_equal(neg, 'neg(SInt<6>("14"))')

    arg = n("a", sw(6))
    neg = Neg(arg, sw(7))
    assert check(neg)
    serialize_equal(neg, 'neg(a)')


def test_type_is_wrong():
    arg = UnknownType()
    neg = Neg(arg, sw(1))
    assert not check(neg)

    arg = vec(sw(10), 8)
    neg = Neg(arg, sw(9))
    assert not check(neg)

    arg = bdl(a=[uw(20), True])
    neg = Neg(arg, sw(21))
    assert not check(neg)


def test_width_is_wrong():
    arg = u(20, w(6))
    neg = Neg(arg, sw(4))
    assert not check(neg)

    arg = n("a", uw(6))
    neg = Neg(arg, sw(6))
    assert not check(neg)

    arg = s(20, w(6))
    neg = Neg(arg, sw(8))
    assert not check(neg)

    arg = n("a", sw(6))
    neg = Neg(arg, sw(6))
    assert not check(neg)
