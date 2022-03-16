from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass, PassException, Error

# Custom Exceptions
class SubfieldNotInBundle(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Subfield {name} is not in bundle.')

class SubfieldOnNonBundle(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Subfield {name} is accessed on non-bundle.')

class IndexTooLarge(PassException):
    def __init__(self, info: Info, mname: str, value: int):
        super().__init__(f'{info}: [module {mname}] Index with value {value} is too large.')

class IndexOnNonVector(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Index illegal on non-vector type.')

class AccessIndexNotUInt(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Access index must be a UInt type')

class IndexNotUInt(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Index is not of UIntType.')

class EnableNotUInt(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Enable is not of UIntType.')

class InvalidConnect(PassException):
    def __init__(self, info: Info, mname: str, cond: str, lhs: Expression, rhs: Expression):
        ltyp = f'\t{lhs.serialize()}: {lhs.typ.serialize()}'
        rtyp = f'\t{rhs.serialize()}: {rhs.typ.serialize()}'
        super().__init__(f'{info}: [module {mname}] Type mismatch in \'{cond}\'.\n{ltyp}\n{rtyp}')

class ReqClk(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Requires a clock typed signal.')

class RegReqClk(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Register {name} requires a clock typed signal.')

class EnNotUInt(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Enable must be a 1-bit UIntType typed signal.')

class PredNotUInt(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Predicate not a 1-bit UIntType.')

class OpNotGround(PassException):
    def __init__(self, info: Info, mname: str, op: str):
        super().__init__(f'{info}: [module {mname}] Primop {op} cannot operate on non-ground types.')

class OpNotUInt(PassException):
    def __init__(self, info: Info, mname: str, op: str, e: str):
        super().__init__(f'{info}: [module {mname}] Primop {op} requires argument {e} to be a UInt type.')

class InvalidRegInit(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Type of init must match type of DefRegister.')

class OpNotAllUInt(PassException):
    def __init__(self, info: Info, mname: str, op: str):
        super().__init__(f'{info}: [module {mname}] Primop {op} requires all arguments to be UInt type.')

class OpNotAllSameType(PassException):
    def __init__(self, info: Info, mname: str, op: str):
        super().__init__(f'{info}: [module {mname}] Primop {op} requires all operands to have the same type.')

class OpNotCorrectType(PassException):
    def __init__(self, info: Info, mname: str, op: str, typs: List[str]):
        super().__init__(f'{info}: [module {mname}] Primop {op} does not have correct arg types: {typs}.')

class NodePassiveType(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Node must be a passive type.')

class MuxSameType(PassException):
    def __init__(self, info: Info, mname: str, t1: str, t2: str):
        super().__init__(f'{info}: [module {mname}] Must mux between equivalent types: {t1} != {t2}.')

class MuxPassiveTypes(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Must mux between passive types.')

class MuxCondUInt(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] A mux condition must be of type 1-bit UInt.')

class MuxClock(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Firrtl does not support muxing clocks.')

class ValidIfPassiveTypes(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Must validif a passive type.')

class ValidIfCondUInt(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}]  A validif condition must be of type UInt.')

class IllegalResetType(PassException):
    def __init__(self, info: Info, mname: str, exp: str):
        super().__init__(f'{info}: [module {mname}] Register resets must have type Reset, AsyncReset, or UInt<1>: {exp}.')

class IllegalUnknownType(PassException):
    def __init__(self, info: Info, mname: str, exp: str):
        super().__init__(f'{info}: [module {mname}]  Uninferred type: {exp}.')

# TODO PrintfArgNotGround | OpNoMixFix | OpNotAnalog | IllegalAnalogDeclaration | IllegalAttachExp
