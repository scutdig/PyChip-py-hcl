from py_hcl.firrtl_ir.stmt.empty import EmptyStmt
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_stmt_equal


def test_empty_serialize():
    serialize_stmt_equal(EmptyStmt(), "skip")
    assert check(EmptyStmt())
