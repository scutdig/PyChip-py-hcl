from pyhcl.ir.low_ir import *
from pyhcl.passes.wir import Flow, SinkFlow, SourceFlow
from typing import List
from pyhcl.passes._pass import PassException

# CheckForm utils
def is_max(w1: Width, w2: Width):
    return IntWidth(max(w1.width, w2.width))

def to_flow(d: Direction) -> Flow:
    if type(d) == Input:
        return SourceFlow()
    if type(d) == Output:
        return SinkFlow()

def flow(e: Expression) -> Flow:
    if type(e) == DoPrim:
        return SourceFlow()
    elif type(e) == UIntLiteral:
        return SourceFlow()
    elif type(e) == SIntLiteral:
        return SourceFlow()
    elif type(e) == Mux:
        return SourceFlow()
    elif type(e) == ValidIf:
        return SourceFlow()
    else:
        raise PassException(f'flow: shouldn\'t be here - {e}')

def mux_type_and_widths(e1, e2) -> Type:
    return mux_type_and_width(e1.typ, e2.typ)

def mux_type_and_width(t1: Type, t2: Type) -> Type:    
    if type(t1) == ClockType and type(t2) == ClockType:
        return ClockType()
    elif type(t1) == AsyncResetType and type(t2) == AsyncResetType:
        return AsyncResetType()
    elif type(t1) == UIntType and type(t2) == UIntType:
        return UIntType(is_max(t1.width, t2.width))
    elif type(t1) == VectorType and type(t2) == VectorType:
        return VectorType(mux_type_and_width(t1.typ, t2.typ), t1.size)
    elif type(t1) == BundleType and type(t2) == BundleType:
        return BundleType(map(lambda f1, f2: Field(f1.name, f1.flip, mux_type_and_width(f1.typ, f2.typ)), list(zip(t1.fields, t2.fields))))
    else:
        return UnknownType

def create_exps(e: Expression) -> List[Expression]:
    if type(e) == Mux:
        e1s = create_exps(e.tval)
        e2s = create_exps(e.fval)
        return list(map(lambda e1, e2: Mux(e.cond, e1, e2, mux_type_and_widths(e1, e2)), list(zip(e1s, e2s))))
    elif type(e) == ValidIf:
        return map(lambda e1: ValidIf(e.cond, e1, e1.typ), create_exps(e.value))
    else:
        if type(e.typ) == GroundType:
            return list(e)
        elif type(e.typ) == BundleType:
            # TODO: add flatMap function
            return list(e)
        elif type(e.typ) == VectorType:
            # TODO: add flatMap function
            return list(e)

def get_info(s: Statement) -> Info:
    if hasattr(s, 'info'):
        return s.info
    else:
        return NoInfo

def has_flip(typ: Type) -> bool:
    if type(typ) == BundleType:
        for f in typ.fields:
            if type(f) == Flip:
                return True
            else:
                return has_flip(f.typ)
    elif type(typ) == VectorType:
        return has_flip(typ.typ)
    else:
        return False

# InterTypes utils

def to_flip(d: Direction):
    if type(d) == Output:
        return Default()
    if type(d) == Input:
        return Flip()

def module_type(m: DefModule) -> BundleType:
    fields = [Field(p.name, to_flip(p.direction), p.typ) for p in m.ports]
    return BundleType(fields)

def field_type(v: Type, s: str) -> Type:
    if type(v) == BundleType:
        def match_type(f: Field) -> Type:
            if f is None:
                return UnknownType
            return  f.typ
        
        for f in v.fields:
            if f.name == s:
                return match_type(f)
    return UnknownType()

def sub_type(v: Type) -> Type:
    if type(v) == VectorType:
        return v.typ
    return UnknownType()

def mux_type(e1: Expression, e2: Expression) -> Type:
    return mux_types(e1.typ, e2.typ)

def mux_types(t1: Type, t2: Type) -> Type:
    if type(t1) == ClockType and type(t2) == ClockType:
        return ClockType()
    elif type(t1) == AsyncResetType and type(t2) == AsyncResetType:
        return AsyncResetType()
    elif type(t1) == UIntType and type(t2) == UIntType:
        return UIntType(UnknownType())
    elif type(t1) == SIntType and type(t2) == SIntType:
        return SIntType(UnknownType())
    elif type(t1) == VectorType and type(t2) == VectorType:
        return VectorType(mux_types(t1.typ, t2.typ), t1.size)
    elif type(t1) == BundleType and type(t2) == BundleType:
        return BundleType(list(map(lambda f1, f2: Field(f1.name, f1.flip, mux_types(f1.typ, f2.typ)), list(zip(t1.fields, t2.fields)))))
    else:
        return UnknownType()

def get_or_else(cond, a, b):
    return a if cond else b