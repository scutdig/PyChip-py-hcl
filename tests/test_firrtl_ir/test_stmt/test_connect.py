from py_hcl.firrtl_ir.shortcuts import n, uw, sw, u, w, s
from py_hcl.firrtl_ir.stmt.connect import Connect
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_stmt_equal


def test_connect_basis():
    cn = Connect(n("a", uw(8)), n("b", uw(8)))
    assert check(cn)
    serialize_stmt_equal(cn, "a <= b")

    cn = Connect(n("a", sw(8)), n("b", sw(8)))
    assert check(cn)
    serialize_stmt_equal(cn, "a <= b")

    cn = Connect(n("a", uw(8)), u(20, w(8)))
    assert check(cn)
    serialize_stmt_equal(cn, 'a <= UInt<8>("h14")')

    cn = Connect(n("a", sw(8)), s(-20, w(8)))
    assert check(cn)
    serialize_stmt_equal(cn, 'a <= SInt<8>("h-14")')


def test_connect_type_wrong():
    cn = Connect(n("a", uw(8)), n("b", sw(8)))
    assert not check(cn)

    cn = Connect(n("a", sw(8)), n("b", uw(8)))
    assert not check(cn)

    cn = Connect(n("a", uw(8)), s(20, w(8)))
    assert not check(cn)

    cn = Connect(n("a", sw(8)), n(-20, w(8)))
    assert not check(cn)
