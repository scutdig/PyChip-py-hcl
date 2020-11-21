import pytest

from py_hcl import Module, IO, U, S, Input, Output
from py_hcl.core.expr.error import ExprError
from py_hcl.core.type.error import TypeError


def test_uint_width_too_small():
    with pytest.raises(TypeError, match='Specified size is invalid'):

        class A(Module):
            io = IO(i=Input(U.w(0)))

    with pytest.raises(TypeError, match='Specified size is invalid'):

        class A(Module):
            io = IO(i=Input(U.w(-42)))


def test_sint_width_too_small():
    with pytest.raises(TypeError, match='Specified size is invalid'):

        class A(Module):
            io = IO(i=Input(S.w(0)))

    with pytest.raises(TypeError, match='Specified size is invalid'):

        class A(Module):
            io = IO(i=Input(S.w(1)))

    with pytest.raises(TypeError, match='Specified size is invalid'):

        class A(Module):
            io = IO(i=Input(S.w(-42)))


def test_uint_lit_out_of_range():
    with pytest.raises(
            ExprError,
            match='Specified value out of range for the given type'):

        class A(Module):
            io = IO(o=Output(U.w(1)))
            io.o <<= U.w(1)(42)


def test_sint_lit_out_of_range():
    with pytest.raises(
            ExprError,
            match='Specified value out of range for the given type'):

        class A(Module):
            io = IO(o=Output(S.w(2)))
            io.o <<= S.w(2)(42)
