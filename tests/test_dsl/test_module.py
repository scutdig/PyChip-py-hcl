import pytest

from py_hcl.core.module_factory import ModuleError
from py_hcl.dsl.expr.expression import Expression
from py_hcl.dsl.expr.io import IO, Input
from py_hcl.dsl.module import Module
from py_hcl.dsl.tpe.hcl_type import HclType


def test_module():
    class A(Module):
        io = IO()
        a = Expression()

    assert hasattr(A, "packed_module")
    assert A.packed_module.name == 'A'
    assert len(A.packed_module.named_expressions) == 4


def test_module_not_contains_io():
    with pytest.raises(ModuleError, match='^.*lack of io.*$'):
        class A(Module):
            b = Expression()


def test_module_inherit():
    class A(Module):
        io = IO()
        a = Expression()

    class B(A):
        io = IO()
        b = Expression()

    assert hasattr(B, "packed_module")
    assert B.packed_module.name == 'B'
    assert len(B.packed_module.named_expressions) == 5


def test_module_duplicate_name():
    with pytest.raises(ModuleError, match='^.*duplicate.*$'):
        class A(Module):
            io = IO()
            a = Expression()

        class B(A):
            io = IO()
            a = Expression()


def test_module_io_duplicate_name():
    with pytest.raises(ModuleError, match='^.*duplicate.*$'):
        class A(Module):
            io = IO(i=Input(HclType()))

        class B(A):
            io = IO(i=Input(HclType()))
