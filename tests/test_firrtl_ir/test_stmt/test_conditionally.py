from py_hcl.firrtl_ir.shortcuts import n, uw, sw, u, w
from py_hcl.firrtl_ir.stmt.block import Block
from py_hcl.firrtl_ir.stmt.conditionally import Conditionally
from py_hcl.firrtl_ir.stmt.connect import Connect
from py_hcl.firrtl_ir.stmt.empty import EmptyStmt
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_stmt_equal


def test_conditionally_basis():
    s1 = EmptyStmt()
    s2 = Connect(n("a", uw(8)), n("b", uw(8)))
    cn = Conditionally(n("a", uw(1)), s1, s2)
    assert check(cn)
    serialize_stmt_equal(cn, "when a :\n"
                             "  skip\n"
                             "else :\n"
                             "  a <= b")

    s1 = Block([
        Connect(n("a", uw(8)), n("b", uw(8))),
        Connect(n("c", sw(8)), n("d", sw(8))),
    ])
    s2 = EmptyStmt()
    cn = Conditionally(u(1, w(1)), s1, s2)
    assert check(cn)
    serialize_stmt_equal(
        cn, 'when UInt<1>("1") :\n'
            '  a <= b\n'
            '  c <= d\n'
            'else :\n'
            '  skip')


def test_conditionally_type_wrong():
    s1 = EmptyStmt()
    s2 = Connect(n("a", uw(8)), n("b", uw(8)))
    cn = Conditionally(n("a", sw(1)), s1, s2)
    assert not check(cn)

    s1 = Block([
        Connect(n("a", uw(8)), n("b", uw(8))),
        Connect(n("c", sw(8)), n("d", sw(8))),
    ])
    s2 = EmptyStmt()
    cn = Conditionally(u(1, w(2)), s1, s2)
    assert not check(cn)
