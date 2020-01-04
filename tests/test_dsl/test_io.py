import pytest

from py_hcl.core.expr import ExprTable
from py_hcl.core.expr.error import ExprError
from py_hcl.core.type.bundle import BundleT
from py_hcl.dsl.expr.io import IO, Input, Output, io_extend
from py_hcl.dsl.module import Module
from py_hcl.core.type import HclType
from py_hcl.dsl.tpe.uint import U


class A(Module):
    io = IO(
        i=Input(U.w(8)),
        o=Output(U.w(8)))

    io.o <<= io.i


def test_io():
    table = A.packed_module.named_expr_chain.named_expr_chain_head \
        .named_expr_holder.named_expression_table
    id = list(table.keys())[list(table.values()).index('io')]
    t = ExprTable.table[id].hcl_type
    assert isinstance(t, BundleT)
    assert len(t.fields) == 2


def test_io_inherit_basis():
    class B(A):
        io = io_extend(A)(
            i1=Input(U.w(9)),
        )
        io.o <<= io.i1

    table = B.packed_module.named_expr_chain.named_expr_chain_head \
        .named_expr_holder.named_expression_table
    id = list(table.keys())[list(table.values()).index('io')]
    t = ExprTable.table[id].hcl_type
    assert isinstance(t, BundleT)
    assert len(t.fields) == 3


def test_io_inherit_override():
    class B(A):
        io = io_extend(A)(
            i=Input(U.w(9)),
        )
        io.o <<= io.i

    table = B.packed_module.named_expr_chain.named_expr_chain_head \
        .named_expr_holder.named_expression_table
    id = list(table.keys())[list(table.values()).index('io')]
    t = ExprTable.table[id].hcl_type
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
