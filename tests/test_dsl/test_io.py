import pytest

from py_hcl.dsl.expr import ExprError
from py_hcl.dsl.expr.io import IO, Input, Output
from py_hcl.dsl.module import Module
from py_hcl.firrtl_ir.expr import Expression


def test_io():
    class A(Module):
        io = IO(
            i=Input(Expression()),
            o=Output(Expression()))

    ps = A.packed_module.named_expressions['io'].ports
    assert len(ps) == 2


def test_io_no_wrap_io():
    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):
            io = IO(i=Expression())

    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):  # noqa: F811
            io = IO(
                i=Expression(),
                o=Output(Expression()))

    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):  # noqa: F811
            io = IO(
                i=Input(Expression()),
                o=Expression())
