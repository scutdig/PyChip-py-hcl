from py_hcl.firrtl_ir.stmt.defn.instance import DefInstance
from py_hcl.firrtl_ir.type_checker import check
from ...utils import serialize_stmt_equal


def test_instance_basis():
    i1 = DefInstance("i1", "ALU")
    assert check(i1)
    serialize_stmt_equal(i1, 'inst i1 of ALU')
