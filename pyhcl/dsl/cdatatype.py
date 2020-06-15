from dataclasses import dataclass
from typing import Optional

from pyhcl.core._repr import CType
from pyhcl.ir import low_ir


@dataclass(eq=False, init=False)
class INT(CType):
    v: int

    def __init__(self, v: int):
        self.v = int(v)


class UInit(type):
    def __call__(cls, v: int):
        return U.w(max(v.bit_length(), 1))(v)


class U(CType, metaclass=UInit):
    def __init__(self, _: int):
        pass

    @staticmethod
    def _lowWidth(width: Optional[int] = None):
        return low_ir.IntWidth(width) if width is not None else None

    @staticmethod
    def w(width: Optional[int] = None):
        """
        Return a UInt type with assigned width
        If width is not given, it would be inferred
        """

        def _mapToIR(_, __=None):
            # If caller is UInt Type, it would call `mapToIR(ctx)`
            # Or caller is UInt Literal, it would call `mapToIR(literal, ctx)`
            if __ is not None:
                return low_ir.UIntLiteral(_.v, U._lowWidth(width))
            else:
                return low_ir.UIntType(U._lowWidth(width))

        def _idxType(_ = None):
            return U.w(1)

        uk = type(f"U?", (INT,), {"mapToIR": _mapToIR, "getIndexedType": _idxType})
        uk.typ = uk

        if width is not None:
            t = type(f"U{width}", (INT,), {"width": width, "mapToIR": _mapToIR, "getIndexedType": _idxType})
            t.typ = uk
            return t
        else:
            return uk


Bool = U.w(1)


class SInit(type):
    def __call__(cls, v: int):
        return S.w(v.bit_length() + 1)(v)


class S(CType, metaclass=SInit):
    def __init__(self, _: int):
        pass

    @staticmethod
    def _lowWidth(width: Optional[int] = None):
        return low_ir.IntWidth(width) if width is not None else None

    @staticmethod
    def w(width: Optional[int] = None):
        """
        Return a UInt type with assigned width
        If width is not given, it would be inferred
        """

        def _mapToIR(_, __=None):
            # If caller is SInt Type, it would call `mapToIR(ctx)`
            # Or caller is SInt Literal, it would call `mapToIR(literal, ctx)`
            if __ is not None:
                return low_ir.SIntLiteral(_.v, S._lowWidth(width))
            else:
                return low_ir.SIntType(S._lowWidth(width))

        def _idxType():
            return S.w(1)

        uk = type(f"S?", (INT,), {"mapToIR": _mapToIR, "getIndexedType": _idxType})
        uk.typ = uk

        if width is not None:
            t = type(f"S{width}", (INT,), {"width": width, "mapToIR": _mapToIR, "getIndexedType": _idxType})
            t.typ = uk
            return t
        else:
            return uk


class Clock(CType):
    def mapToIR(self, ctx):
        return low_ir.ClockType()
