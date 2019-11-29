from py_hcl.core.stmt_factory.connect import Connect
from py_hcl.dsl.expr.expression import Expression
from py_hcl.dsl.expr.io import IO
from py_hcl.dsl.module import Module


def test_statement():
    class A(Module):
        io = IO()

        a = Expression()
        b = Expression()
        c = Expression()

        c <<= a + b

    s = A.packed_module.top_scope.statements
    assert len(s) == 1
    assert isinstance(s[0]['statement'], Connect)
