from py_hcl.firrtl_ir.shortcuts import uw, bdl, sw
from py_hcl.firrtl_ir.stmt.defn.wire import DefWire
from py_hcl.firrtl_ir.type_checker import check
from ...utils import serialize_stmt_equal


def test_wire_basis():
    wire = DefWire("w1", uw(8))
    assert check(wire)
    serialize_stmt_equal(wire, 'wire w1 : UInt<8>')

    wire = DefWire("w2", bdl(a=(uw(8), True), b=(sw(8), False)))
    assert check(wire)
    serialize_stmt_equal(wire, 'wire w2 : {flip a : UInt<8>, b : SInt<8>}')
