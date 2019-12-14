import pytest

from py_hcl.core.stmt.error import StatementError
from py_hcl.core.stmt.connect import Connect
from py_hcl.core.stmt.scope import ScopeType
from py_hcl.dsl.branch import when, else_when, otherwise
from py_hcl.core.expr import HclExpr
from py_hcl.dsl.expr.io import IO
from py_hcl.dsl.module import Module


def test_branch():
    class A(Module):
        io = IO()
        a = HclExpr()
        b = HclExpr()
        c = HclExpr()

        a <<= b
        with when(HclExpr()):
            a <<= b + c
            c <<= a
        with else_when(HclExpr()):
            b <<= a + c
            with when(HclExpr()):
                b <<= a
            with otherwise():
                c <<= a
        with otherwise():
            c <<= a + b

    s = A.packed_module.top_scope.statements
    assert len(s) == 4

    assert s[0]['scope']['scope_type'] == ScopeType.GROUND
    assert isinstance(s[0]['statement'], Connect)

    assert s[1]['scope']['scope_type'] == ScopeType.WHEN
    assert s[1]['scope']['scope_level'] == 2
    assert len(s[1]['statement']) == 2

    assert s[2]['scope']['scope_type'] == ScopeType.ELSE_WHEN
    assert s[2]['scope']['scope_level'] == 2
    assert len(s[2]['statement']) == 3
    assert s[2]['statement'][1]['scope']['scope_type'] == ScopeType.WHEN
    assert s[2]['statement'][1]['scope']['scope_level'] == 3
    assert s[2]['statement'][2]['scope']['scope_type'] == ScopeType.OTHERWISE
    assert s[2]['statement'][2]['scope']['scope_level'] == 3

    assert s[3]['scope']['scope_type'] == ScopeType.OTHERWISE
    assert s[3]['scope']['scope_level'] == 2
    assert len(s[3]['statement']) == 1


def test_branch_syntax_error1():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = HclExpr()
            b = HclExpr()
            c = HclExpr()

            a <<= b
            with else_when(HclExpr()):
                b <<= a + c
            with otherwise():
                c <<= a + b


def test_branch_syntax_error2():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = HclExpr()
            b = HclExpr()
            c = HclExpr()

            with otherwise():
                c <<= a + b


def test_branch_syntax_error3():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = HclExpr()
            b = HclExpr()
            c = HclExpr()

            with when(HclExpr()):
                b <<= a + c
                with otherwise():
                    c <<= a + b


def test_branch_syntax_error4():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = HclExpr()
            b = HclExpr()
            c = HclExpr()

            with when(HclExpr()):
                b <<= a + c
                with else_when(HclExpr()):
                    c <<= a + b
            with otherwise():
                c <<= a + b


def test_branch_syntax_error5():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = HclExpr()
            b = HclExpr()
            c = HclExpr()

            with when(HclExpr()):
                b <<= a + c
            c <<= a + b
            with otherwise():
                c <<= a + b
