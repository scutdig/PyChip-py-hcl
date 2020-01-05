from multipledispatch import dispatch

from py_hcl.core.type import HclType


@dispatch()
def invert_exp(self: HclType):
    from py_hcl.core.type.bundle import Dir
    return {'dir': Dir.SINK, 'hcl_type': self}


def bd_fld_wrap(cls):
    if hasattr(cls, '__invert__'):
        return cls

    cls.__invert__ = invert_exp
    return cls


@dispatch()
def vec_exp(self: HclType, i: int):
    from py_hcl.core.type.vector import VectorT
    return VectorT(self, i)


@dispatch()
def vec_exp(self: HclType, t: tuple):
    from py_hcl.core.type.vector import VectorT

    # TODO: Accurate Error Message
    assert all(isinstance(i, int) for i in t)
    v = self
    for s in t[::-1]:
        v = VectorT(v, s)
    return v


def vec_wrap(cls):
    if hasattr(cls, '__getitem__'):
        return cls

    cls.__getitem__ = vec_exp
    return cls
