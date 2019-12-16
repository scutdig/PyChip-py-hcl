from py_hcl.firrtl_ir.shortcuts import n, uw, u, w
from py_hcl.firrtl_ir.stmt.block import Block
from py_hcl.firrtl_ir.stmt.conditionally import Conditionally
from py_hcl.firrtl_ir.stmt.connect import Connect
from py_hcl.firrtl_ir.stmt.defn.circuit import DefCircuit
from py_hcl.firrtl_ir.stmt.defn.module import DefModule, OutputPort, InputPort
from py_hcl.firrtl_ir.stmt.defn.node import DefNode
from py_hcl.firrtl_ir.stmt.empty import EmptyStmt
from py_hcl.firrtl_ir.type_checker import check
from tests.test_firrtl_ir.utils import serialize_stmt_equal


def test_circuit_basis():
    m1 = DefModule("m1", [OutputPort("p", uw(8))],
                   Connect(n("p", uw(8)), u(2, w(8))))

    m2 = DefModule("m2", [InputPort("b", uw(8)),
                          OutputPort("a", uw(8))],
                   Block([DefNode("n", u(1, w(1))),
                          Conditionally(n("n", uw(1)),
                                        EmptyStmt(),
                                        Connect(n("a", uw(8)), n("b", uw(8))))]
                         ))
    ct = DefCircuit("m1", [m1, m2])
    assert check(ct)
    serialize_stmt_equal(ct, 'circuit m1 :\n'
                             '  module m1 :\n'
                             '    output p : UInt<8>\n'
                             '\n'
                             '    p <= UInt<8>("2")\n'
                             '\n'
                             '  module m2 :\n'
                             '    input b : UInt<8>\n'
                             '    output a : UInt<8>\n'
                             '\n'
                             '    node n = UInt<1>("1")\n'
                             '    when n :\n'
                             '      skip\n'
                             '    else :\n'
                             '      a <= b\n'
                             '\n')


def test_circuit_module_not_exist():
    m1 = DefModule("m1", [OutputPort("p", uw(8))],
                   Connect(n("p", uw(8)), u(2, w(8))))

    m2 = DefModule("m2", [InputPort("b", uw(8)),
                          OutputPort("a", uw(8))],
                   Block([DefNode("n", u(1, w(1))),
                          Conditionally(n("n", uw(1)),
                                        EmptyStmt(),
                                        Connect(n("a", uw(8)), n("b", uw(8))))]
                         ))
    ct = DefCircuit("m3", [m1, m2])
    assert not check(ct)


def test_circuit_module_wrong():
    m1 = DefModule("m1", [OutputPort("p", uw(8))],
                   Connect(n("p", uw(8)), u(2, w(8))))
    m2 = DefModule("m2", [], Connect(n("p", uw(8)), u(2, w(8))))
    ct = DefCircuit("m1", [m1, m2])
    assert not check(ct)
