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
            if isinstance(e, Reference):
                return Reference(e.name, get_or_else(e.name in typs.keys(), typs[e.name], UnknownType))
            elif isinstance(e, SubField):
                return SubField(e.expr, e.name, field_type(e.expr.typ, e.name))
            elif isinstance(e, SubIndex):
                return SubIndex(e.name, e.expr, e.value, sub_type(e.expr.typ))
            elif isinstance(e, SubAccess):
                return SubAccess(e.expr, e.index, sub_type(e.expr.typ))
            elif isinstance(e, DoPrim):
                return DoPrim(e.op, e.args, e.consts, e.typ)
            elif isinstance(e, Mux):
                return Mux(e.cond, e.tval, e.fval, mux_type(e.tval, e.fval))
            elif isinstance(e, ValidIf):
                return ValidIf(e.cond, e.value, e.value.typ)
            else:
                return e
        
        def infer_types_s(typs: Dict[str, Type], s: Statement) -> Statement:
            if isinstance(s, DefRegister):
                typs[s.name] = s.typ
                clock = infer_types_e(typs, s.clock) if hasattr(s, 'clock') and isinstance(s.clock, Expression) else None
                reset = infer_types_e(typs, s.reset) if hasattr(s, 'reset') and isinstance(s.reset, Expression) else None
                init = infer_types_e(typs, s.init) if hasattr(s, 'init') and isinstance(s.init, Expression) else None
                return DefRegister(s.name, s.typ, clock, reset, init, s.info)
            elif isinstance(s, DefWire):
                typs[s.name] = s.typ
                return s
            elif isinstance(s, DefNode):
                value = infer_types_e(typs, s.value) if hasattr(s, 'value') and isinstance(s.value, Expression) else None
                typs[s.name] = s.value.typ
                return DefNode(s.name, value, s.info)
            elif isinstance(s, DefMemory):
                typs[s.name] = s.memType
                return s
            elif isinstance(s, DefInstance):
                typs[s.name] = mtyps[s.module]
                return s
            else:
                return s

        
        def infer_types_p(typs: set, p: Port) -> Port:
            typs[p.name] = p.typ
            return p
        
        def infer_types(m: DefModule) -> DefModule:
            if isinstance(m, ExtModule):
                return m
            types: Dict[str, Type] = {}
            ports = None
            stmts = None
            if hasattr(m, 'ports') and isinstance(m.ports, list):
                ports = list(map(lambda p: infer_types_p(types, p), m.ports))
            
            if hasattr(m, 'body') and isinstance(m.body, Block):
                if hasattr(m.body, 'stmts') and isinstance(m.body.stmts, list):
                    stmts = list(map(lambda s: infer_types_s(types, s), m.body.stmts))
                    
            return Module(m.name, ports, Block(stmts), m.typ, m.info)
        
        res = list(map(lambda m: infer_types(m), c.modules))
        return Circuit(res, c.main, c.info)