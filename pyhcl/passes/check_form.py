from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass, PassException, Error
from pyhcl.passes.utils import ModuleGraph, to_flow, flow, create_exps, get_info, has_flip
from pyhcl.passes.wir import *


# ScopeView
class ScopeView:
    def __init__(self, moduleNS: set, scopes: List[set]):
        self.moduleNS = moduleNS
        self.scopes = scopes
    
    def declare(self, name: str):
        self.moduleNS.add(name)
        self.scopes[0].add(name)
    
    # ensures that the name cannot be used again, but prevent references to this name
    def add_to_namespace(self, name: str):
        self.moduleNS.add(name)

    def expand_m_port_visibility(self, port: DefMemPort):
        mem_in_scopes = False
        def expand_m_port(scope: set, mp: DefMemPort):
            if mp.mem.name in scope:
                scope.add(mp.name)
            return scope
        self.scopes = list(map(lambda scope: expand_m_port(scope, port), self.scopes))
        for sx in self.scopes:
            if port.mem.name in sx:
                mem_in_scopes = True
        if mem_in_scopes is False:
            self.scopes[0].add(port.name)

    
    def legal_decl(self, name: str) -> bool:
        return name in self.moduleNS

    def legal_ref(self, name: str) -> bool:
        for s in self.scopes:
            if name in s:
                return True
        return False

    def child_scope(self):
        return ScopeView(self.moduleNS, [])

def scope_view():
    return ScopeView(set(), [set()])


# Custom Exceptions
class NotUniqueException(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Reference {name} does not have a unique name.')
class InvalidLOCException(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Invalid connect to an expression that is not a reference or a WritePort.')

class NegUIntException(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] UIntLiteral cannot be negative.')

class UndecleardReferenceException(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Reference {name} is not declared.')

class PoisonWithFlipException(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Poison {name} cannot be a bundle type with flips.')

class MemWithFlipException(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Memory {name} cannot be a bundle type with flips.')

class IllegalMemLatencyException(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Memory {name} must have non-negative read latency and positive write latency.')

class RegWithFlipException(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: [module {mname}] Register {name} cannot be a bundle type with flips.')

class InvalidAccessException(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Invalid access to non-reference.')

class ModuleNameNotUniqueException(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: Repeat definition of module {mname}')

class DefnameConflictException(PassException):
    def __init__(self, info: Info, mname: str, defname: str):
        super().__init__(f'{info}: defname {defname} of extmodule {mname} conflicts with an existing module.')

class DefnameDifferentPortsException(PassException):
    def __init__(self, info: Info, mname: str, defname: str):
        super().__init__(f'{info}: ports of extmodule {mname} with defname {defname} are different for an extmodule with the same defname.')

class DefnameDifferentPortsException(PassException):
    def __init__(self, info: Info, name: str):
        super().__init__(f'{info}: Module {name} is not defined.')

class IncorrectNumArgsException(PassException):
    def __init__(self, info: Info, mname: str, op: str, n: int):
        super().__init__(f'{info}: [module {mname}] Primop {op} requires {n} expression arguments.')

class IncorrectNumConstsException(PassException):
    def __init__(self, info: Info, mname: str, op: str, n: int):
        super().__init__(f'{info}: [module {mname}] Primop {op} requires {n} integer arguments.')

class NegWidthException(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Width cannot be negative.')

class NegVecSizeException(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Vector type size cannot be negative.')

class NegMemSizeException(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: [module {mname}] Memory size cannot be negative or zero.')

class InstanceLoop(PassException):
    def __init__(self, info: Info, mname: str, loop: str):
        super().__init__(f'{info}: [module {mname}] Has instance loop {loop}.')

class NoTopModuleException(PassException):
    def __init__(self, info: Info, name: str):
        super().__init__(f'{info}: A single module must be named {name}.')

class NegArgException(PassException):
    def __init__(self, info: Info, mname: str, op: str, value: int):
        super().__init__(f'{info}: [module {mname}] Primop {op} argument {value} < 0.')

class LsbLargerThanMsbException(PassException):
    def __init__(self, info: Info, mname: str, op: str, lsb: int, msb: int):
        super().__init__(f'{info}: [module {mname}] Primop {op} lsb {lsb} > {msb}.')
  
class ResetInputException(PassException):
    def __init__(self, info: Info, mname: str, expr: Expression):
        super().__init__(f'{info}: [module {mname}] Abstract Reset not allowed as top-level input: {expr.serialize()}')

class ResetExtModuleOutputException(PassException):
    def __init__(self, info: Info, mname: str, expr: Expression):
        super().__init__(f'{info}: [module {mname}] Abstract Reset not allowed as ExtModule output: {expr.serialize()}')

class ModuleNotDefinedException(PassException):
    def __init__(self, info: Info, mname: str, name: str):
        super().__init__(f'{info}: Module {name} is not defined.')

class CircuitHasNoModules(PassException):
    def __init__(self, info: Info, cname: str):
        super().__init__(f'{info}: Circuit {cname} has no modules.')

class ModuleHasNoPorts(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: Module {mname} has no ports.')

class ModuleHasNoBody(PassException):
    def __init__(self, info: Info, mname: str):
        super().__init__(f'{info}: Module {mname} has no body.')

class CheckHighForm(Pass):
    def __init__(self, c: Circuit):
        self.c: Circuit = c
        self.ms: List[DefModule] = c.modules
        self.module_names: List[str] = [_.name for _ in c.modules]
        self.int_module_name: List[str] = [_.name for _ in c.modules if isinstance(_, Module)]
        self.errors: Error = Error()
    
    def check_unique_module_name(self):
        for idx in range(len(self.module_names)):
            if self.int_module_name[idx] in self.int_module_name[idx:]:
                m = self.ms[idx]
                self.errors.append(ModuleNameNotUniqueException(m.info, m.name))
    
    def check_extmodule(self):
        for m in self.ms:
            if isinstance(m, ExtModule) and m.name in self.int_module_name:
                self.errors.append(DefnameConflictException(m.info, m.name, m.defname))

    def strip_width(self, typ: Type) -> Type:
        if isinstance(typ, GroundType):
            return typ.map_width(UnknownWidth)
        elif isinstance(typ, AggregateType):
            return typ.map_type(self.strip_width())

    def check_highForm_primOp(self, info: Info, mname: str, e: DoPrim):
        def correct_num(ne, nc):
            if isinstance(ne, int) and len(e.args) != ne:
                self.errors.append(IncorrectNumArgsException(info, mname, e.op.serialize(), ne))
            
            if len(e.consts) != nc:
                self.errors.append(IncorrectNumConstsException(info, mname, e.op.serialize(), nc))
        
        def non_negative_consts():
            for _ in [c for c in e.consts if c < 0]:
                self.errors.append(NegArgException(info, mname, e.op.serialize(), _))
        
        if isinstance(e.op, (Add, Sub, Mul, Div, Rem, Lt, Leq, Gt, Geq, Eq, Neq, Dshl, Dshr, And, Or, Xor, Cat)):
            correct_num(2, 0)
        elif isinstance(e.op, (AsUInt, AsSInt, AsClock, Cvt, Neq, Not)):
            correct_num(1, 0)
        elif isinstance(e.op, AsFixedPoint):
            correct_num(1, 1)
        elif isinstance(e.op, (Shl, Shr, Pad, Head, Tail)):
            correct_num(1, 1)
            non_negative_consts()
        elif isinstance(e.op, Bits):
            correct_num(1, 2)
            non_negative_consts()
            if len(e.consts) == 2:
                msb, lsb = e.consts[0], e.consts[1]
                if msb > lsb:
                    self.errors.append(LsbLargerThanMsbException(info, mname, e.op.serialize(), lsb, msb))
        elif isinstance(e.op, (Andr, Orr, Xorr, Neg)):
            correct_num(1, 0)
    
    def check_valid_loc(self, info: Info, mname: str, e: Expression):
        if isinstance(e, (UIntLiteral, SIntLiteral, DoPrim)):
            self.errors.append(InvalidLOCException(info, mname))
    
    def check_instance(self, info: Info, child: str, parent: str):
        if child not in self.module_names:
            self.errors.append(ModuleNotDefinedException(info, parent, child))
        childToParent = ModuleGraph().add(parent, child)
        if childToParent is not None and len(childToParent) > 0:
            self.errors.append(InstanceLoop(info, parent, "->".join(childToParent)))
    
    def check_high_form_w(self, info: Info, mname: str, w: Width):
        if isinstance(w, IntWidth) and w.width < 0:
            self.errors.append(NegWidthException(info, mname))
    
    def check_high_form_t(self, info: Info, mname: str, typ: Type):
        t_attr = typ.__dict__.items()
        for _, ta in t_attr:
            if isinstance(ta, Type):
                self.check_high_form_t(info, mname, ta)
            if isinstance(ta, Width):
                    self.check_high_form_w(info, mname, ta)
        
        if isinstance(typ, VectorType) and typ.size < 0:
            self.errors.append(NegVecSizeException(info, mname))
                
    def valid_sub_exp(self, info: Info, mname: str, e: Expression):
        if isinstance(e, (Reference, SubField, SubIndex, SubAccess)):
            ...
        elif isinstance(e, (Mux, ValidIf)):
            ...
        else:
            self.errors.append(InvalidAccessException(info, mname))

    def check_high_form_e(self, info: Info, mname: str, names: ScopeView, e: Expression):
        e_attr = e.__dict__.items()
        if isinstance(e, Reference) and names.legal_ref(e.name) is False:
            self.errors.append(UndecleardReferenceException(info, mname, e.name))
        elif isinstance(e, UIntLiteral) and e.value < 0:
            self.errors.append(NegUIntException(info, mname, e.name))
        elif isinstance(e, DoPrim):
            self.check_highForm_primOp(info, mname, e)
        elif isinstance(e, (Reference, UIntLiteral, Mux, ValidIf)):
            ...
        elif isinstance(e, SubAccess):
            self.valid_sub_exp(info, mname, e.expr)
        else:
            for _, ea in e_attr:
                if isinstance(ea, Expression):
                    self.valid_sub_exp(info, mname, ea)
        
        for _, ea in e_attr:
            if isinstance(ea, Width):
                self.check_high_form_w(info, mname + '/' + e.serialize(), ea)
            if isinstance(ea, Expression):
                self.check_high_form_e(info, mname, names, ea)
    
    def check_name(self, info: Info, mname: str, names: ScopeView, referenced: bool, s: Statement):
        if referenced is False:
            return
        if len(s.name) == 0:
            assert referenced is False, 'A statement with an empty name cannot be used as a reference!'
        else:
            if names.legal_decl(s.name) is True:
                self.errors.append(NotUniqueException(info, mname, s.name))
            if referenced:
                names.declare(s.name)
            else:
                names.add_to_namespace(s.name)
    
    def check_high_form_s(self, minfo: Info, mname: str, names: ScopeView, s: Statement):
        s_attr = s.__dict__.items()
        t_info = get_info(s)
        info = t_info if isinstance(t_info, NoInfo) is False else minfo
        referenced = True if isinstance(s, (DefWire, DefRegister, DefInstance, DefMemory, DefNode, Port)) else False
        self.check_name(info, mname, names, referenced, s)
        if isinstance(s, DefRegister):
            if has_flip(s.typ):
                self.errors.append(RegWithFlipException(info, mname, s.name))
        elif isinstance(s, DefMemory):
            if has_flip(s.memType.typ):
                self.errors.append(MemWithFlipException(info, mname, s.name))
            if s.memType.size < 0:
                self.errors.append(NegMemSizeException(info, mname))
        elif isinstance(s, DefInstance):
            self.check_instance(info, mname, s.module)
        elif isinstance(s, Connect):
            self.check_valid_loc(info, mname, s.loc)
        elif isinstance(s, DefMemPort):
            names.expand_m_port_visibility(s)
        else:
            ...

        for _, sa in s_attr:
            if isinstance(sa, Type):
                self.check_high_form_t(info, mname, sa)
            elif isinstance(sa, Expression):
                self.check_high_form_e(info, mname, names, sa)

        if isinstance(s, Conditionally):
            self.check_high_form_s(minfo, mname, names.child_scope(), s.conseq)
            self.check_high_form_s(minfo, mname, names.child_scope(), s.alt)
        else:
            for _, sa in s_attr:
                if isinstance(sa, Statement):
                    self.check_high_form_s(minfo, mname, names, sa)


    
    def check_high_form_p(self, mname: str, names: ScopeView, p: Port):
        if names.legal_decl(p.name) is True:
            self.errors.append(NotUniqueException(NoInfo, mname, p.name))
        names.declare(p.name)
        self.check_high_form_t(p.info, mname, p.typ)
    
    def find_bad_reset_type_ports(self, m: DefModule, dir: Direction):
        bad_reset_type_ports = []
        bad = to_flow(dir)
        gen = ((create_exps(ref), p1) for (ref, p1) in [(Reference(p.name, p.typ), p) for p in m.ports])
        for expr, port in gen:
            if isinstance(expr, list):
                for exx in expr:
                    if exx is not None and exx.typ == ResetType and flow(exx) == bad:
                        bad_reset_type_ports.append((port, exx))
            else:
                if expr is not None and expr.typ == ResetType and flow(expr) == bad:
                    bad_reset_type_ports.append((port, expr))
            
        
        return bad_reset_type_ports
    
    def check_high_form_m(self, m: DefModule):
        names = scope_view()
        if hasattr(m, 'ports') and isinstance(m.ports, list):
            for p in m.ports:
                self.check_high_form_p(m.name, names, p)
        else:
            self.errors.append(ModuleHasNoPorts(m.info, m.name))
        
        if hasattr(m, 'body') and isinstance(m.body, Block):
            if hasattr(m.body, 'stmts') and isinstance(m.body.stmts, list):
                for s in m.body.stmts:
                    self.check_high_form_s(m.info, m.name, names, s)
            else:
                self.errors.append(ModuleHasNoBody(m.info, m.name))
        
        if isinstance(m, ExtModule):
            for port, expr in self.find_bad_reset_type_ports(m, Output):
                self.errors.append(ResetExtModuleOutputException(port.info, m.name, expr))

    def run(self):
        if hasattr(self.c, 'modules') and isinstance(self.c.modules, list):
            for m in self.c.modules:
                self.check_high_form_m(m)
        else:
            self.errors.append(CircuitHasNoModules(self.c.info, self.c.main))

        if self.c.main not in self.int_module_name:
            self.errors.append(NoTopModuleException(self.c.info, self.c.main))               
        
        self.errors.trigger()
        return self.c
