from py_hcl.firrtl_ir.expr.prim_ops import Bits
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    arg = u(20, w(5))
    bits = Bits(arg, [4, 4], uw(1))
    assert check(bits)
    serialize_equal(bits, 'bits(UInt<5>("14"), 4, 4)')

    arg = u(20, w(5))
    bits = Bits(arg, [4, 2], uw(3))
    assert check(bits)
    serialize_equal(bits, 'bits(UInt<5>("14"), 4, 2)')

    arg = n("a", uw(6))
    bits = Bits(arg, [4, 2], uw(3))
    assert check(bits)
    serialize_equal(bits, 'bits(a, 4, 2)')

    arg = s(20, w(6))
    bits = Bits(arg, [4, 2], uw(3))
    assert check(bits)
    serialize_equal(bits, 'bits(SInt<6>("14"), 4, 2)')

    arg = n("a", sw(6))
    bits = Bits(arg, [4, 2], uw(3))
    assert check(bits)
    serialize_equal(bits, 'bits(a, 4, 2)')


def test_type_is_wrong():
    arg = UnknownType()
    bits = Bits(arg, [4, 2], uw(3))
    assert not check(bits)

    arg = vec(sw(10), 8)
    bits = Bits(arg, [6, 2], uw(5))
    assert not check(bits)

    arg = bdl(a=[uw(20), True])
    bits = Bits(arg, [18, 2], uw(17))
    assert not check(bits)


def test_width_is_wrong():
    arg = u(20, w(5))
    bits = Bits(arg, [4, 2], uw(2))
    assert not check(bits)

    arg = n("a", uw(6))
    bits = Bits(arg, [4, 2], uw(4))
    assert not check(bits)

    arg = s(20, w(6))
    bits = Bits(arg, [4, 2], uw(2))
    assert not check(bits)

    arg = n("a", sw(6))
    bits = Bits(arg, [4, 2], uw(4))
    assert not check(bits)


def test_over_bound():
    arg = u(20, w(5))
    bits = Bits(arg, [5, 2], uw(4))
    assert not check(bits)

    arg = n("a", uw(5))
    bits = Bits(arg, [2, -1], uw(4))
    assert not check(bits)

    arg = s(20, w(6))
    bits = Bits(arg, [7, 4], uw(4))
    assert not check(bits)

    arg = n("a", sw(6))
    bits = Bits(arg, [2, -1], uw(4))
    assert not check(bits)
