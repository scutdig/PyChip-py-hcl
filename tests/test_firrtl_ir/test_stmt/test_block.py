from py_hcl.firrtl_ir.shortcuts import u, w, n, uw
from py_hcl.firrtl_ir.stmt.block import Block
from py_hcl.firrtl_ir.stmt.conditionally import Conditionally
from py_hcl.firrtl_ir.stmt.connect import Connect
from py_hcl.firrtl_ir.stmt.defn.node import DefNode
from py_hcl.firrtl_ir.stmt.empty import EmptyStmt
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_stmt_equal


def test_block_basis():
    blk = Block([EmptyStmt()])
    assert check(blk)
    serialize_stmt_equal(blk, "skip")

    blk = Block([DefNode("n", u(1, w(1))),
                 Conditionally(n("n", uw(1)),
                               EmptyStmt(),
                               Connect(n("a", uw(8)), n("b", uw(8))))
                 ])
    assert check(blk)
    serialize_stmt_equal(blk, 'node n = UInt<1>("h1")\n'
                              'when n :\n'
                              '  skip\n'
                              'else :\n'
                              '  a <= b')


def test_block_empty():
    blk = Block([])
    assert not check(blk)
