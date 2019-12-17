import pytest

from py_hcl.core.module_factory.error import ModuleError
from py_hcl.core.expr import HclExpr
from py_hcl.dsl.expr.io import IO, Input
from py_hcl.dsl.module import Module
from py_hcl.core.type import HclType


def test_module():
    class A(Module):
        io = IO()
        a = HclExpr()

    assert hasattr(A, "packed_module")
    assert A.packed_module.name == 'A'
    assert len(A.packed_module.named_expressions) == 2


def test_module_not_contains_io():
    with pytest.raises(ModuleError, match='^.*lack of io.*$'):
        class A(Module):
            b = HclExpr()


def test_module_inherit():
    class A(Module):
        io = IO()
        a = HclExpr()

    class B(A):
        io = IO()
        b = HclExpr()

    assert hasattr(B, "packed_module")
    assert B.packed_module.name == 'B'
    assert len(B.packed_module.named_expressions) == 3


def test_module_duplicate_name():
    with pytest.raises(ModuleError, match='^.*duplicate.*$'):
        class A(Module):
            io = IO()
            a = HclExpr()

        class B(A):
            io = IO()
            a = HclExpr()


def test_module_io_duplicate_name():
    with pytest.raises(ModuleError, match='^.*duplicate.*$'):
        class A(Module):
            io = IO(i=Input(HclType()))

        class B(A):
            io = IO(i=Input(HclType()))
