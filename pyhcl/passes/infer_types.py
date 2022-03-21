from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass
from pyhcl.passes.wir import *
from pyhcl.passes.utils import module_type, field_type, sub_type, mux_type, get_or_else

class InferTypes(Pass):
    def run(self, c: Circuit) -> Circuit:
        mtyps: Dict[str, Type] = {}
        for m in c.modules:
            mtyps[m.name] = module_type(m)

        def infer_types_e(typs: Dict[str, Type], e: Expression) -> Expression:
            if type(e) == Expression:
                return infer_types_e(typs, e)
            elif type(e) == Reference:
                return Reference(e.name, get_or_else(e.name in typs.keys(), typs[e.name], UnknownType))
            elif type(e) == SubField:
                return SubField(e.expr, e.name, field_type(e.expr.typ, e.name))
            elif type(e) == SubIndex:
                return SubIndex(e.name, e.expr, e.value, sub_type(e.expr.typ))
            elif type(e) == SubAccess:
                return SubAccess(e.expr, e.index, sub_type(e.expr.typ))
            elif type(e) == DoPrim:
                return DoPrim(e.op, e.args, e.consts, UnknownType())
            elif type(e) == Mux:
                return Mux(e.cond, e.tval, e.fval, mux_type(e.tval, e.fval))
            elif type(e) == ValidIf:
                return ValidIf(e.cond, e.value, e.value.typ)
            else:
                return e
        
        def infer_types_s(typs: Dict[str, Type], s: Statement) -> Statement:
            if type(s) == DefRegister:
                typs[s.name] = s.typ
                for _, e in s.__dict__.items():
                    if type(e) == Expression:
                        s[_] = infer_types_e(typs, e)
                return s
            elif type(s) == DefWire:
                typs[s.name] = s.typ
                return s
            elif type(s) == DefNode:
                for _, e in s.__dict__.items():
                    if type(e) == Expression:
                        s[_] = infer_types_e(typs, e)
                typs[s.name] = s.value.typ
                return s
            elif type(s) == DefMemory:
                typs[s.name] = DefMemPort(s.name, _, _, _, _, NoInfo())
                return s
            elif type(s) == DefInstance:
                typs[s.name] = mtyps[s.name]
                return s
            else:
                s_attr = s.__dict__.items()
                for _, sa in s_attr:
                    if type(sa) == Statement:
                        s[_] = infer_types_s(typs, sa)
                    if type(sa) == Expression:
                        s[_] = infer_types_e(typs, sa)
                return s

        
        def infer_types_p(typs: set, p: Port) -> Port:
            typs[p.name] = p.typ
            return p
        
        def infer_types(m: DefModule) -> DefModule:
            types = Dict[str, Type]
            m_attr = m.__dict__.items()
            for mk, ma in m_attr:
                if mk == 'ports':
                    for p in ma:
                        infer_types_p(types, p)
                if mk == 'body':
                    for s in ma.stmt:
                        infer_types_s(types, s)
        
        return Circuit(list(map(lambda m: infer_types(m), c.modules)), c.main, c.info)