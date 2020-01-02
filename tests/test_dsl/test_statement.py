from py_hcl.core.stmt.connect import Connect
from py_hcl.dsl.expr.io import IO
from py_hcl.dsl.expr.wire import Wire
from py_hcl.dsl.module import Module
from py_hcl.dsl.tpe.uint import U


def test_statement():
    class A(Module):
        io = IO()

        a = Wire(U.w(8))
        b = Wire(U.w(8))
        c = Wire(U.w(8))

        c <<= a + b

    s = A.packed_module.statement_chain \
        .stmt_chain_head.stmt_holder.top_statement.statements
    assert len(s) == 1
    assert isinstance(s[0].statement, Connect)
