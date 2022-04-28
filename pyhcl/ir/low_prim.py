import logging
from abc import ABC
from dataclasses import dataclass

from pyhcl.ir.low_node import FirrtlNode


class PrimOp(FirrtlNode, ABC):
    """Primitive Operation"""

    def serialize(self) -> str:
        return self.__repr__()

    def verilog_op(self):
        logging.error(f"No {self.__repr__()} in verilog")
        exit(-1)

    def verilog_serialize(self) -> str:
        return self.verilog_op()


@dataclass(frozen=True, init=False)
class Add(PrimOp):
    """Addition"""

    def __repr__(self):
        return 'add'

    def verilog_op(self):
        return " + "


# Subtraction
@dataclass(frozen=True, init=False)
class Sub(PrimOp):
    def __repr__(self):
        return 'sub'

    def verilog_op(self):
        return " - "


# Multiplication
@dataclass(frozen=True, init=False)
class Mul(PrimOp):
    def __repr__(self):
        return 'mul'

    def verilog_op(self):
        return " * "


# Division
@dataclass(frozen=True, init=False)
class Div(PrimOp):
    def __repr__(self):
        return 'div'

    def verilog_op(self):
        return " / "


# Remainder
@dataclass(frozen=True, init=False)
class Rem(PrimOp):
    def __repr__(self):
        return 'rem'

    def verilog_op(self):
        return " % "


# Less Than
@dataclass(frozen=True, init=False)
class Lt(PrimOp):
    def __repr__(self):
        return 'lt'

    def verilog_op(self):
        return " < "



# Less Than Or Equal To
@dataclass(frozen=True, init=False)
class Leq(PrimOp):
    def __repr__(self):
        return 'leq'

    def verilog_op(self):
        return " <= "


# Greater Than
@dataclass(frozen=True, init=False)
class Gt(PrimOp):
    def __repr__(self):
        return 'gt'

    def verilog_op(self):
        return " > "


# Greater Than Or Equal To
@dataclass(frozen=True, init=False)
class Geq(PrimOp):
    def __repr__(self):
        return 'geq'

    def verilog_op(self):
        return " >= "


# Equal To
@dataclass(frozen=True, init=False)
class Eq(PrimOp):
    def __repr__(self):
        return 'eq'

    def verilog_op(self):
        return " == "


# Not Equal To
@dataclass(frozen=True, init=False)
class Neq(PrimOp):
    def __repr__(self):
        return 'neq'


    def verilog_op(self):
        return " != "


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

    def verilog_op(self):
        return " << "


# Static Shift Right
@dataclass(frozen=True, init=False)
class Shr(PrimOp):
    def __repr__(self):
        return 'shr'

    def verilog_op(self):
        return " >> "


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

    def verilog_op(self):
        return " - "


# Bitwise Complement
@dataclass(frozen=True, init=False)
class Not(PrimOp):
    def __repr__(self):
        return 'not'

    def verilog_op(self):
        return " ~ "


# Bitwise And
@dataclass(frozen=True, init=False)
class And(PrimOp):
    def __repr__(self):
        return 'and'

    def verilog_op(self):
        return " & "


# Bitwise Or
@dataclass(frozen=True, init=False)
class Or(PrimOp):
    def __repr__(self):
        return 'or'

    def verilog_op(self):
        return " | "


# Bitwise Exclusive Or
@dataclass(frozen=True, init=False)
class Xor(PrimOp):
    def __repr__(self):
        return 'xor'

    def verilog_op(self):
        return " ^ "


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
    
    def verilog_op(self):
        return self.__repr__()


# Bit Extraction
@dataclass(frozen=True, init=False)
class Bits(PrimOp):
    def __repr__(self):
        return 'bits'
    
    def verilog_op(self):
        return self.__repr__()


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
