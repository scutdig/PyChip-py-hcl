from py_hcl.firrtl_ir.stmt.empty import EmptyStmt
from ..utils import serialize_stmt_equal


def test_empty_serialize():
    serialize_stmt_equal(EmptyStmt(), "skip")
