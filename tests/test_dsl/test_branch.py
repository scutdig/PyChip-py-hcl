import pytest

from py_hcl.core.stmt import ConditionStatement
from py_hcl.core.stmt.connect import Connect
from py_hcl.core.stmt.error import StatementError
from py_hcl.core.stmt_factory.scope import ScopeType, ScopeManager
from py_hcl.dsl.branch import when, else_when, otherwise
from py_hcl.dsl.expr.io import IO
from py_hcl.dsl.expr.wire import Wire
from py_hcl.dsl.module import Module
from py_hcl.dsl.tpe.uint import U


def test_branch():
    class A(Module):
        io = IO()
        a = Wire(U.w(8))
        b = Wire(U.w(8))
        c = Wire(U.w(8))

        a <<= b
        with when(U(0)):
            a <<= b + c
            c <<= a
        with else_when(U(1)):
            b <<= a + c
            with when(U(0)):
                b <<= a
            with otherwise():
                c <<= a
        with otherwise():
            c <<= a + b
            c <<= a + b
            c <<= a + b
            c <<= a + b

    s = A.packed_module.statement_chain \
        .stmt_chain_head.stmt_holder.top_statement.statements
    assert len(s) == 2

    si = ScopeManager.get_scope_info(s[0].scope_id)
    assert si.scope_type == ScopeType.GROUND
    assert isinstance(s[0].statement, Connect)

    assert isinstance(s[1], ConditionStatement)
    assert len(s[1].seq_stmts) == 2

    assert len(s[1].alt_stmts) == 1
    assert isinstance(s[1].alt_stmts[0], ConditionStatement)
    assert len(s[1].alt_stmts[0].seq_stmts) == 2
    assert len(s[1].alt_stmts[0].alt_stmts) == 4

    assert isinstance(s[1].alt_stmts[0].seq_stmts[1], ConditionStatement)
    assert len(s[1].alt_stmts[0].seq_stmts[1].seq_stmts) == 1
    assert len(s[1].alt_stmts[0].seq_stmts[1].alt_stmts) == 1


def test_branch_syntax_error1():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = Wire(U.w(8))
            b = Wire(U.w(8))
            c = Wire(U.w(8))

            a <<= b
            with else_when(U(0)):
                b <<= a + c
            with otherwise():
                c <<= a + b


def test_branch_syntax_error2():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = Wire(U.w(8))
            b = Wire(U.w(8))
            c = Wire(U.w(8))

            with otherwise():
                c <<= a + b


def test_branch_syntax_error3():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = Wire(U.w(8))
            b = Wire(U.w(8))
            c = Wire(U.w(8))

            with when(U(0)):
                b <<= a + c
                with otherwise():
                    c <<= a + b


def test_branch_syntax_error4():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = Wire(U.w(8))
            b = Wire(U.w(8))
            c = Wire(U.w(8))

            with when(U(0)):
                b <<= a + c
                with else_when(U(1)):
                    c <<= a + b
            with otherwise():
                c <<= a + b


def test_branch_syntax_error5():
    with pytest.raises(StatementError):
        class A(Module):
            io = IO()
            a = Wire(U.w(8))
            b = Wire(U.w(8))
            c = Wire(U.w(8))

            with when(U(0)):
                b <<= a + c
            c <<= a + b
            with otherwise():
                c <<= a + b
