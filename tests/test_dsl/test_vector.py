import pytest

from py_hcl import Module, IO, U, Input
from py_hcl.core.type.error import TypeError


def test_vec_size_too_small():
    with pytest.raises(TypeError, match='Specified size is invalid'):

        class A(Module):
            io = IO(i=Input(U.w(8)[0]))

    with pytest.raises(TypeError, match='Specified size is invalid'):

        class A(Module):
            io = IO(i=Input(U.w(8)[-42]))
