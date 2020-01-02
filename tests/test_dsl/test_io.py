import pytest

from py_hcl.core.expr import ExprPool
from py_hcl.core.expr.error import ExprError
from py_hcl.core.type.bundle import BundleT
from py_hcl.dsl.expr.io import IO, Input, Output
from py_hcl.dsl.module import Module
from py_hcl.core.type import HclType
from py_hcl.dsl.tpe.uint import U


def test_io():
    class A(Module):
        io = IO(
            i=Input(U.w(8)),
            o=Output(U.w(8)))

        io.o <<= io.i

    t = A.packed_module.named_expr_chain.named_expr_chain_head \
        .named_expr_holder.named_expressions['io']
    t = ExprPool.pool[t['expr_id']].hcl_type
    assert isinstance(t, BundleT)
    assert len(t.fields) == 2


def test_io_no_wrap_io():
    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):
            io = IO(i=HclType())

    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):
            io = IO(
                i=HclType(),
                o=Output(HclType()))

    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):
            io = IO(
                i=Input(HclType()),
                o=HclType())
