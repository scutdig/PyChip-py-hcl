import pytest

from py_hcl.core.expr import HclExpr
from py_hcl.core.module_factory.error import ModuleError
from py_hcl.dsl.expr.io import IO
from py_hcl.dsl.module import Module


def test_module():
    class A(Module):
        io = IO()
        a = HclExpr()

    assert hasattr(A, "packed_module")
    assert len(A.packed_module.named_expr_chain.named_expr_chain_head
               .named_expr_holder.named_expression_table) == 2


def test_module_not_contains_io():
    with pytest.raises(ModuleError, match='^.*lack of io.*$'):
        class A(Module):
            b = HclExpr()
