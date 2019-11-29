import pytest

from py_hcl.core.module_constructor import ModuleErr
from py_hcl.dsl.expression import Expression
from py_hcl.dsl.module import Module


def test_module():
    class A(Module):
        io = Expression()
        a = Expression()

    assert hasattr(A, "packed_module")
    assert A.packed_module.name == 'A'
    assert len(A.packed_module.named_expressions) == 4


def test_module_not_contains_io():
    with pytest.raises(ModuleErr, match='not contains io'):
        class A(Module):
            b = Expression()


def test_module_inherit():
    class A(Module):
        io = Expression()
        a = Expression()

    class B(A):
        io = Expression()
        b = Expression()

    assert hasattr(B, "packed_module")
    assert B.packed_module.name == 'B'
    assert len(B.packed_module.named_expressions) == 5


def test_module_duplicate_name():
    with pytest.raises(ModuleErr, match='duplicate names'):
        class A(Module):
            io = Expression()
            a = Expression()

        class B(A):
            io = Expression()
            a = Expression()
