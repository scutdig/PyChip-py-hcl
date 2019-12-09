import pytest

from py_hcl.dsl.expr import ExprError
from py_hcl.dsl.expr.io import IO, Input, Output
from py_hcl.dsl.module import Module
from py_hcl.dsl.tpe.hcl_type import HclType


def test_io():
    class A(Module):
        io = IO(
            i=Input(HclType()),
            o=Output(HclType()))

    ps = A.packed_module.named_expressions['io'].ports
    assert len(ps) == 4


def test_io_no_wrap_io():
    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):
            io = IO(i=HclType())

    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):  # noqa: F811
            io = IO(
                i=HclType(),
                o=Output(HclType()))

    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):  # noqa: F811
            io = IO(
                i=Input(HclType()),
                o=HclType())
