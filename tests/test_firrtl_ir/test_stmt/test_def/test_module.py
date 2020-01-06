from py_hcl.firrtl_ir.shortcuts import uw, n, w, u, s
from py_hcl.firrtl_ir.stmt.block import Block
from py_hcl.firrtl_ir.stmt.conditionally import Conditionally
from py_hcl.firrtl_ir.stmt.connect import Connect
from py_hcl.firrtl_ir.stmt.defn.module import DefModule, \
    OutputPort, InputPort, DefExtModule
from py_hcl.firrtl_ir.stmt.defn.node import DefNode
from py_hcl.firrtl_ir.stmt.empty import EmptyStmt
from py_hcl.firrtl_ir.type_checker import check
from ...utils import serialize_stmt_equal


def test_module_basis():
    mod = DefModule("m", [OutputPort("p", uw(8))],
                    Connect(n("p", uw(8)), u(2, w(8))))
    assert check(mod)
    serialize_stmt_equal(mod, 'module m :\n'
                              '  output p : UInt<8>\n'
                              '\n'
                              '  p <= UInt<8>("h2")')

    mod = DefModule("m", [InputPort("b", uw(8)),
                          OutputPort("a", uw(8))],
                    Block([DefNode("n", u(1, w(1))),
                           Conditionally(n("n", uw(1)),
                                         EmptyStmt(),
                                         Connect(n("a", uw(8)), n("b", uw(8))))
                           ]))
    assert check(mod)
    serialize_stmt_equal(mod, 'module m :\n'
                              '  input b : UInt<8>\n'
                              '  output a : UInt<8>\n'
                              '\n'
                              '  node n = UInt<1>("h1")\n'
                              '  when n :\n'
                              '    skip\n'
                              '  else :\n'
                              '    a <= b')


def test_module_empty_ports():
    mod = DefModule("m", [], Connect(n("p", uw(8)), u(2, w(8))))
    assert not check(mod)


def test_module_body_wrong():
    mod = DefModule("m", [OutputPort("p", uw(8))],
                    Connect(n("p", uw(8)), s(2, w(8))))
    assert not check(mod)


def test_ext_module_basis():
    mod = DefExtModule("em", [InputPort("b", uw(8)),
                              OutputPort("a", uw(8))], "em")
    assert check(mod)
    serialize_stmt_equal(mod, 'extmodule em :\n'
                              '  input b : UInt<8>\n'
                              '  output a : UInt<8>\n'
                              '\n'
                              '  defname = em')


def test_ext_module_empty_ports():
    mod = DefExtModule("em", [], "em")
    assert not check(mod)
