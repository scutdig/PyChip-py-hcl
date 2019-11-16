from py_hcl.firrtl_ir.expr.prim_ops import Lt
from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_basis():
    args = [u(20, w(5)), u(15, w(4))]
    lt = Lt(args, uw(1))
    assert check(lt)
    serialize_equal(lt, 'lt(UInt<5>("14"), UInt<4>("f"))')

    args = [n("a", uw(6)), u(15, w(4))]
    lt = Lt(args, uw(1))
    assert check(lt)
    serialize_equal(lt, 'lt(a, UInt<4>("f"))')

    args = [n("a", uw(6)), n("b", uw(6))]
    lt = Lt(args, uw(1))
    assert check(lt)
    serialize_equal(lt, 'lt(a, b)')

    args = [s(20, w(6)), s(15, w(5))]
    lt = Lt(args, uw(1))
    assert check(lt)
    serialize_equal(lt, 'lt(SInt<6>("14"), SInt<5>("f"))')

    args = [n("a", sw(6)), s(-15, w(5))]
    lt = Lt(args, uw(1))
    assert check(lt)
    serialize_equal(lt, 'lt(a, SInt<5>("-f"))')

    args = [n("a", sw(6)), n("b", sw(6))]
    lt = Lt(args, uw(1))
    assert check(lt)
    serialize_equal(lt, 'lt(a, b)')


def test_type_is_wrong():
    args = [n("a", UnknownType()), n("b", sw(6))]
    lt = Lt(args, uw(1))
    assert not check(lt)

    args = [n("a", uw(6)), n("b", UnknownType())]
    lt = Lt(args, uw(1))
    assert not check(lt)

    args = [n("a", vec(sw(10), 8)), n("b", sw(6))]
    lt = Lt(args, uw(1))
    assert not check(lt)

    args = [n("a", uw(6)), n("b", bdl(a=[uw(20), True]))]
    lt = Lt(args, uw(1))
    assert not check(lt)


def test_width_is_wrong():
    args = [n("a", sw(6)), n("b", sw(6))]
    lt = Lt(args, uw(6))
    assert not check(lt)

    args = [n("a", uw(6)), n("b", uw(6))]
    lt = Lt(args, uw(6))
    assert not check(lt)

    args = [n("b", sw(6)), n("a", sw(6))]
    lt = Lt(args, uw(0))
    assert not check(lt)

    args = [n("a", uw(6)), n("b", uw(6))]
    lt = Lt(args, uw(10))
    assert not check(lt)
