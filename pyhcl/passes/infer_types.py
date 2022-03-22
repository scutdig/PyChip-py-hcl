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
            if isinstance(e, Expression):
                return infer_types_e(typs, e)
            elif isinstance(e, Reference):
                return Reference(e.name, get_or_else(e.name in typs.keys(), typs[e.name], UnknownType))
            elif isinstance(e, SubField):
                return SubField(e.expr, e.name, field_type(e.expr.typ, e.name))
            elif isinstance(e, SubIndex):
                return SubIndex(e.name, e.expr, e.value, sub_type(e.expr.typ))
            elif isinstance(e, SubAccess):
                return SubAccess(e.expr, e.index, sub_type(e.expr.typ))
            elif isinstance(e, DoPrim):
                return DoPrim(e.op, e.args, e.consts, UnknownType())
            elif isinstance(e, Mux):
                return Mux(e.cond, e.tval, e.fval, mux_type(e.tval, e.fval))
            elif isinstance(e, ValidIf):
                return ValidIf(e.cond, e.value, e.value.typ)
            else:
                return e
        
        def infer_types_s(typs: Dict[str, Type], s: Statement) -> Statement:
            if isinstance(s, DefRegister):
                typs[s.name] = s.typ
                for _, e in s.__dict__.items():
                    if isinstance(e, Expression):
                        s[_] = infer_types_e(typs, e)
                return s
            elif isinstance(s, DefWire):
                typs[s.name] = s.typ
                return s
            elif isinstance(s, DefNode):
                for _, e in s.__dict__.items():
                    if isinstance(e, Expression):
                        s[_] = infer_types_e(typs, e)
                typs[s.name] = s.value.typ
                return s
            elif isinstance(s, DefMemory):
                typs[s.name] = DefMemPort(s.name, _, _, _, _, NoInfo())
                return s
            elif isinstance(s, DefInstance):
                typs[s.name] = mtyps[s.name]
                return s
            else:
                s_attr = s.__dict__.items()
                for _, sa in s_attr:
                    if isinstance(sa, Statement):
                        s[_] = infer_types_s(typs, sa)
                    if isinstance(sa, Expression):
                        s[_] = infer_types_e(typs, sa)
                return s

        
        def infer_types_p(typs: set, p: Port) -> Port:
            typs[p.name] = p.typ
            return p
        
        def infer_types(m: DefModule) -> DefModule:
            types = Dict[str, Type]
            if hasattr(m, 'ports') and isinstance(m.ports, list):
                for p in m.ports:
                    infer_types_p(types, p)
            
            if hasattr(m, 'body') and isinstance(m.body, Block):
                if hasattr(m.body, 'stmts') and isinstance(m.body.stmts, list):
                    for s in m.body.stmts:
                        infer_types_s(types, s)
        
        return Circuit(list(map(lambda m: infer_types(m), c.modules)), c.main, c.info)