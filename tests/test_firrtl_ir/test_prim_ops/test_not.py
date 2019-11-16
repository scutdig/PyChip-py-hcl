from py_hcl.firrtl_ir.expr.prim_ops import Not
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    arg = u(20, w(5))
    simple_not = Not(arg, uw(5))
    assert check(simple_not)
    serialize_equal(simple_not, 'not(UInt<5>("14"))')

    arg = n("a", uw(6))
    simple_not = Not(arg, uw(6))
    assert check(simple_not)
    serialize_equal(simple_not, 'not(a)')

    arg = s(20, w(6))
    simple_not = Not(arg, uw(6))
    assert check(simple_not)
    serialize_equal(simple_not, 'not(SInt<6>("14"))')

    arg = n("a", sw(6))
    simple_not = Not(arg, uw(6))
    assert check(simple_not)
    serialize_equal(simple_not, 'not(a)')


def test_type_is_wrong():
    arg = UnknownType()
    simple_not = Not(arg, uw(1))
    assert not check(simple_not)

    arg = vec(sw(10), 8)
    simple_not = Not(arg, uw(8))
    assert not check(simple_not)

    arg = bdl(a=[uw(20), True])
    simple_not = Not(arg, uw(20))
    assert not check(simple_not)


def test_width_is_wrong():
    arg = u(20, w(5))
    simple_not = Not(arg, uw(4))
    assert not check(simple_not)

    arg = n("a", uw(6))
    simple_not = Not(arg, uw(7))
    assert not check(simple_not)

    arg = s(20, w(6))
    simple_not = Not(arg, uw(5))
    assert not check(simple_not)

    arg = n("a", sw(6))
    simple_not = Not(arg, uw(7))
    assert not check(simple_not)
