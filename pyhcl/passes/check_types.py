from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass, PassException, Error
from pyhcl.passes.utils import times_f_f
from pyhcl.passes.wir import WrappedType

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

class CheckTypes(Pass):
    def legal_reset_type(self, typ: Type) -> bool:
        if type(typ) == UIntType and type(typ.width) == IntWidth:
            return typ.width.width == 1
        elif type(typ) == AsyncResetType:
            return True
        elif type(typ) == ResetType:
            return True
        else:
            return False
    
    def legal_cond_type(self, typ: Type) -> bool:
        if  type(typ) == UIntType and type(typ.width) == IntWidth:
            return typ.width.width == 1
        elif type(type) == UIntType:
            return True
        else:
            return False
    
    def bulk_equals(self, t1: Type, t2: Type, flip1: Orientation, flip2: Orientation) -> bool:
        if type(t1) == ClockType and type(t2) == ClockType:
            return flip1 == flip2
        elif type(t1) == UIntType and type(t2) == UIntType:
            return flip1 == flip2
        elif type(t1) == SIntType and type(t2) == SIntType:
            return flip1 == flip2
        elif type(t1) == AsyncResetType and type(t2) == AsyncResetType:
            return flip1 == flip2
        elif type(t1) == ResetType:
            return self.legal_reset_type(t2) and flip1 == flip2
        elif type(t2) == ResetType:
            return self.legal_reset_type(t1) and flip1 == flip2
        elif type(t1) == BundleType and type(t2) == BundleType:
            t1_fields = {}
            for f1 in t1.fields:
                t1_fields[f1.name] = (f1.typ, f1.flip)
            for f2 in f2.fields:
                if f2.name in t1_fields.keys():
                    t1_flip = t1_fields[f2.name].typ
                    return self.bulk_equals(t1_flip, f2.typ, times_f_f(flip1, t1_flip) ,times_f_f(flip2, f2.flip))
                else:
                    return True
        elif type(t1) == VectorType and type(t2) == VectorType:
            return self.bulk_equals(t1.typ, t2.typ, flip1, flip2)
        else:
            return False
    
    def valid_connect(self, locTyp: Type, exprTyp: Type) -> bool:
        # TODO
        ...

    def valid_connects(self, c: Connect) -> bool:
        return self.valid_connect(c.loc.typ, c.expr.typ)
    
    def run(self, c: Circuit):
        errors = Error()

        def passive(t: Type) -> bool:
            if type(t) in [UIntType, SIntType]:
                return True
            elif type(t) == VectorType:
                return passive(t.typ)
            elif type(t) == BundleType:
                final = True
                for f in t.fields:
                    final = f.flip == Default and passive(f.typ) and final
                return final
            else:
                return True
        
        def check_typs_primop(info: Info, mname: str, e: DoPrim):
            def check_all_typs(exprs: List[Expression], okUInt: bool, okSInt: bool, okClock: bool, okAsync: bool):
                for expr in exprs:
                    if type(expr.typ) == UIntType and okUInt is False:
                        errors.append(OpNotCorrectType(info, mname, e.op.serialize(), [expr.typ.serialize() for expr in exprs]))
                    elif type(expr.typ) == SIntType and okSInt is False:
                        errors.append(OpNotCorrectType(info, mname, e.op.serialize(), [expr.typ.serialize() for expr in exprs]))
                    elif type(expr.typ) == ClockType and okClock is False:
                        errors.append(OpNotCorrectType(info, mname, e.op.serialize(), [expr.typ.serialize() for expr in exprs]))
                    elif type(expr.typ) == AsyncResetType and okAsync is False:
                        errors.append(OpNotCorrectType(info, mname, e.op.serialize(), [expr.typ.serialize() for expr in exprs]))
                
                if type(e.op) in [AsUInt, AsSInt, AsClock, AsyncResetType]:
                    # TODO
                    ...
                elif type(e.op) in [Dshl, Dshr]:
                    check_all_typs(list(e.args[0]), True, True, False, False)
                    check_all_typs(e.args[1:], True, False, False, False)
                elif type(e.op) in [Add, Sub, Mul, Lt, Leq, Gt, Geq, Eq, Neq]:
                    check_all_typs(e.args, True, True, False, False)
                elif type(e.op) in [Pad, Bits, Head, Tail]:
                    check_all_typs(e.args, True, True, False, False)
                elif type(e.op) in [Shr, Shl, Cat]:
                    check_all_typs(e.args, True, True, False, False)
                else:
                    check_all_typs(e.args, True, True, False, False)
        
        def check_types_e(info: Info, mname: str, e: Expression):
            if type(e) == DoPrim:
                check_typs_primop(info, mname, e)
            elif type(e) == Mux:
                if WrappedType(e.tval.typ) != WrappedType(e.fval.typ):
                    errors.append(MuxSameType(info, mname, e.tval.typ.serialize(), e.fval.typ.serialize()))
                if passive(e.typ) is False:
                    errors.append(MuxPassiveTypes(info, mname))
                if self.legal_cond_type(e.cond.typ) is False:
                    errors.append(MuxCondUInt(info, mname))
            elif type(e) == ValidIf:
                if passive(e.typ) is False:
                    errors.append(ValidIfPassiveTypes(info, mname))
                if type(e.cond.typ) == UIntType:
                    # TODO
                    ...
                else:
                    errors.append(ValidIfCondUInt(info, mname))
            else:
                # TODO
                ...
            
            for _, ee in e.__dict__.items():
                if type(ee) == Expression:
                    check_types_e(info, mname, ee)
        
        def check_types_s(minfo: Info, mname: str, s: Statement):
            def get_info(s):
                if type(s) == NoInfo:
                    return minfo
                else:
                    return s
            
            if type(s) == Connect and self.valid_connects(s) is False:
                con_msg = Connect(s.loc, s.expr, NoInfo()).serialize()
                errors.append(InvalidConnect(get_info(s), mname, con_msg, s.loc, s.expr))
            elif type(s) == DefRegister:
                if WrappedType(s.typ) != WrappedType(s.init.typ):
                    errors.append(InvalidRegInit(get_info(s), mname))
                if self.valid_connect(s.typ, s.init.typ) is False:
                    con_msg = Connect(s.loc, s.expr, NoInfo()).serialize()
                    errors.append(InvalidConnect(get_info(s), mname, con_msg, Reference(s.name, s.typ), s.init))
                
                if self.legal_reset_type(s.reset.typ) is False:
                    errors.append(IllegalResetType(get_info(s), mname, s.name))
                if type(s.clock.typ) != UIntType or type(s.clock.typ.width) != IntWidth or s.clock.typ.width.width != 1:
                    errors.append(RegReqClk(get_info(s), mname, s.name))
            elif type(s) == Conditionally and self.legal_cond_type(s.pred.typ) is False:
                errors.append(PredNotUInt(get_info(s), mname))
            elif type(s) == DefNode:
                if passive(s.value.typ) is False:
                    errors.append(NodePassiveType(get_info(s), mname))
            elif type(s) == DefMemory:
                # TODO
                ...
            else:
                # TODO
                ...
            
            for _, ss in s.__dict__.items():
                if type(ss) == Statement:
                    check_types_s(get_info(s), mname, ss)
                if type(ss) == Expression:
                    check_types_e(get_info(s), mname, ss)
        
        for m in c.modules:
            if hasattr(m, 'body') and type(m.body) == Block:
                if hasattr(m.body, 'stmts') and type(m.body.stmts) == list:
                    for s in m.body.stmts:
                        check_types_s(m.info, m.name, s)
        
        errors.trigger()
        return c