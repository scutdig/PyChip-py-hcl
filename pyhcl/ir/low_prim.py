from abc import ABC
from dataclasses import dataclass

from pyhcl.ir.low_node import FirrtlNode


class PrimOp(FirrtlNode, ABC):
    """Primitive Operation"""

    def serialize(self) -> str:
        return self.__repr__()


@dataclass(frozen=True, init=False)
class Add(PrimOp):
    """Addition"""

    def __repr__(self):
        return 'add'


# Subtraction
@dataclass(frozen=True, init=False)
class Sub(PrimOp):
    def __repr__(self):
        return 'sub'


# Multiplication
@dataclass(frozen=True, init=False)
class Mul(PrimOp):
    def __repr__(self):
        return 'mul'


# Division
@dataclass(frozen=True, init=False)
class Div(PrimOp):
    def __repr__(self):
        return 'div'


# Remainder
@dataclass(frozen=True, init=False)
class Rem(PrimOp):
    def __repr__(self):
        return 'rem'


# Less Than
@dataclass(frozen=True, init=False)
class Lt(PrimOp):
    def __repr__(self):
        return 'lt'


# Less Than Or Equal To
@dataclass(frozen=True, init=False)
class Leq(PrimOp):
    def __repr__(self):
        return 'leq'


# Greater Than
@dataclass(frozen=True, init=False)
class Gt(PrimOp):
    def __repr__(self):
        return 'gt'


# Greater Than Or Equal To
@dataclass(frozen=True, init=False)
class Geq(PrimOp):
    def __repr__(self):
        return 'geq'


# Equal To
@dataclass(frozen=True, init=False)
class Eq(PrimOp):
    def __repr__(self):
        return 'eq'


# Not Equal To
@dataclass(frozen=True, init=False)
class Neq(PrimOp):
    def __repr__(self):
        return 'neq'


# Padding
@dataclass(frozen=True, init=False)
class Pad(PrimOp):
    def __repr__(self):
        return 'pad'


# Interpret As UInt
@dataclass(frozen=True, init=False)
class AsUInt(PrimOp):
    def __repr__(self):
        return 'asUInt'


# Interpret As SInt
@dataclass(frozen=True, init=False)
class AsSInt(PrimOp):
    def __repr__(self):
        return 'asSInt'


# Interpret As Clock
@dataclass(frozen=True, init=False)
class AsClock(PrimOp):
    def __repr__(self):
        return 'asClock'


# Static Shift Left
@dataclass(frozen=True, init=False)
class Shl(PrimOp):
    def __repr__(self):
        return 'shl'


# Static Shift Right
@dataclass(frozen=True, init=False)
class Shr(PrimOp):
    def __repr__(self):
        return 'shr'


# Dynamic Shift Left
@dataclass(frozen=True, init=False)
class Dshl(PrimOp):
    def __repr__(self):
        return 'dshl'


# Dynamic Shift Right
@dataclass(frozen=True, init=False)
class Dshr(PrimOp):
    def __repr__(self):
        return 'dshr'


# Arithmetic Convert to Signed
@dataclass(frozen=True, init=False)
class Cvt(PrimOp):
    def __repr__(self):
        return 'cvt'


# Negate
@dataclass(frozen=True, init=False)
class Neg(PrimOp):
    def __repr__(self):
        return 'neg'


# Bitwise Complement
@dataclass(frozen=True, init=False)
class Not(PrimOp):
    def __repr__(self):
        return 'not'


# Bitwise And
@dataclass(frozen=True, init=False)
class And(PrimOp):
    def __repr__(self):
        return 'and'


# Bitwise Or
@dataclass(frozen=True, init=False)
class Or(PrimOp):
    def __repr__(self):
        return 'or'


# Bitwise Exclusive Or
@dataclass(frozen=True, init=False)
class Xor(PrimOp):
    def __repr__(self):
        return 'xor'


# Bitwise And Reduce
@dataclass(frozen=True, init=False)
class Andr(PrimOp):
    def __repr__(self):
        return 'andr'


# Bitwise Or Reduce
@dataclass(frozen=True, init=False)
class Orr(PrimOp):
    def __repr__(self):
        return 'orr'


# Bitwise Exclusive Or Reduce
@dataclass(frozen=True, init=False)
class Xorr(PrimOp):
    def __repr__(self):
        return 'xorr'


# Concatenate
@dataclass(frozen=True, init=False)
class Cat(PrimOp):
    def __repr__(self):
        return 'cat'


# Bit Extraction
@dataclass(frozen=True, init=False)
class Bits(PrimOp):
    def __repr__(self):
        return 'bits'


# Head
@dataclass(frozen=True, init=False)
class Head(PrimOp):
    def __repr__(self):
        return 'head'


# Tail
@dataclass(frozen=True, init=False)
class Tail(PrimOp):
    def __repr__(self):
        return 'tail'


# Interpret as Fixed Point
@dataclass(frozen=True, init=False)
class AsFixedPoint(PrimOp):
    def __repr__(self):
        return 'asFixedPoint'


# Shift Binary Point Left
@dataclass(frozen=True, init=False)
class BPShl(PrimOp):
    def __repr__(self):
        return 'bpshl'


# Shift Binary Point Right
@dataclass(frozen=True, init=False)
class BPShr(PrimOp):
    def __repr__(self):
        return 'bpshr'


# Set Binary Point
@dataclass(frozen=True, init=False)
class BPSet(PrimOp):
    def __repr__(self):
        return 'bpset'
