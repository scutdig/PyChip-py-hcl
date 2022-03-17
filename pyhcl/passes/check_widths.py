from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass, PassException, Error

# MaxWidth
maxWidth = 1000000

class UninferredWidth(PassException):
    def __init__(self, info: Info, target: str):
        super().__init__(f'{info}:  Uninferred width for target below. (Did you forget to assign to it?) \n{target}')

class InvalidRange(PassException):
    def __init__(self, info: Info, target: str, i: Type):
        super().__init__(f'{info}: Invalid range {i.serialize()} for target below. (Are the bounds valid?) \n{target}')

class  WidthTooSmall(PassException):
    def __init__(self, info: Info, mname: str, b: int):
        super().__init__(f'{info} : [target {mname}]  Width too small for constant {b}.')

class WidthTooBig(PassException):
    def __init__(self, info: Info, mname: str, b: int):
        super().__init__(f'{info} : [target ${mname}]  Width {b} greater than max allowed width of {maxWidth} bits')       

class DshlTooBig(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info} : [target {mname}]  Width of dshl shift amount must be less than {maxWidth} bits.')

class MultiBitAsClock(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info} : [target {mname}]  Cannot cast a multi-bit signal to a Clock.')

class MultiBitAsAsyncReset(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info} : [target {mname}]  Cannot cast a multi-bit signal to an AsyncReset.')

class NegWidthException(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [target {mname}] Width cannot be negative or zero.')

class BitsWidthException(PassException):
    def __init__(self, info: Info, mname: str, hi: int, width: int, exp: str):
        super().__init__(f'{info}: [target {mname}] High bit {hi} in bits operator is larger than input width {width} in {exp}.')

class HeadWidthException(PassException):
    def __init__(self, info: Info, mname: str, n: int, width: int):
        super().__init__(f'{info}: [target {mname}] Parameter {n} in head operator is larger than input width {width}.')

class TailWidthException(PassException):
    def __init__(self, info: Info, mname: str, n: int, width: int):
        super().__init__(f'{info}: [target {mname}] Parameter {n} in tail operator is larger than input width {width}.')

class CheckWidths(Pass):
    def run(self, c: Circuit):
        errors = Error()

        def check_width_w(info: Info, target: str, t: Type, w: Width):
            if type(w) == IntWidth and w.width >= maxWidth:
                errors.append(WidthTooBig(info, target, w.width))
            elif type(w) == IntWidth:
                ...
            else:
                errors.append(UninferredWidth(info, target))
        
        def has_width(typ: Type) -> bool:
            if type(typ) == GroundType and hasattr(typ, 'width') and type(typ.width) == IntWidth:
                return True
            elif type(typ) == GroundType:
                return False
            else:
                raise PassException(f'hasWidth - {typ}')
        
        def check_width_t(info: Info, target: str, t: Type):
            if type(t) == BundleType:
                ...
        
        def check_width_s(minfo: Info, target: str, s: Statement):
            ...
        
        def check_width_p(minfo: Info, target: str, p: Port):
            ...
        
        def check_width_m(target: str, m: DefModule):
            for mk, ma in m.__dict__.items():
                if type(ma) == List[Port] and mk == 'ports':
                    for p in ma:
                        check_width_p(m.info, target + m.name, p)
                if type(ma) == Block and mk == 'body':
                    for s in ma.stmts:
                        check_width_s(m.info, target + m.name, s)
        
        for m in c.modules:
            check_width_m(c.main, m)
        
        errors.trigger()
        return c
