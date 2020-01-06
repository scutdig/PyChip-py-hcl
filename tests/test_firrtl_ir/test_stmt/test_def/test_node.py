from py_hcl.firrtl_ir.expr.accessor import SubIndex
from py_hcl.firrtl_ir.shortcuts import n, s, w, vec, uw
from py_hcl.firrtl_ir.stmt.defn.node import DefNode
from py_hcl.firrtl_ir.type_checker import check
from ...utils import serialize_stmt_equal


def test_node_basis():
    node = DefNode("n1", s(20, w(6)))
    assert check(node)
    serialize_stmt_equal(node, 'node n1 = SInt<6>("h14")')

    node = DefNode("n2", SubIndex(n("v", vec(uw(8), 10)), 7, uw(8)))
    assert check(node)
    serialize_stmt_equal(node, 'node n2 = v[7]')


def test_node_expr_wrong():
    node = DefNode("n1", s(20, w(5)))
    assert not check(node)

    node = DefNode("n2", SubIndex(n("v", vec(uw(8), 10)), 10, uw(8)))
    assert not check(node)
