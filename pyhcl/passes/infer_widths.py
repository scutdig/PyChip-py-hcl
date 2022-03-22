from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass
from pyhcl.passes.wir import *

class InferTypes(Pass):
    @staticmethod
    def run(c: Circuit):
        def infer_widths_t(widths: Dict[str, Width], name: str, t: Type) -> tuple[Type, List[Width]]:
            if isinstance(t, BundleType):
                bs = list(map(lambda f: infer_widths_t(widths, name, f.typ) if f.name == name else None, t.fields))
                bs = [b for b in bs if b is not None].pop()
                t, widths = bs[0], bs[1]

            if isinstance(t, VectorType):
                return infer_widths_t(widths, name, t.typ)

            if isinstance(t, UIntType):
                if isinstance(t.width, UnknownWidth):
                    return UIntType(widths.values().pop()), widths.clear()
                else:
                    widths[name] = t.width
            if isinstance(t, SIntType):
                if isinstance(t.width, UnknownWidth):
                    return SIntType(widths.values().pop()), widths.clear()
                else:
                    widths[name] = t.width
            
            return t, widths
        
        def infer_widths_p(widths: Dict[str, Width], p: Port):
            t, widths = infer_widths_t(widths, p.name, p.typ)
            return Port(p.name, p.direction, t), widths

        def infer_widths_e(widths: Dict[str, Width], e: Expression):
            t, widths = infer_widths_t(widths, e.name, e.typ)
            if isinstance(e, SubField):
                return SubField(e.expr, e.name, t), widths
            elif isinstance(e, SubAccess):
                return SubAccess(e.expr, e.index, t), widths
            elif isinstance(e, SubIndex):
                return SubIndex(e.name, e.expr, e.value, t), widths
            elif isinstance(e, DoPrim):
                return DoPrim(e.op, e.args, e.consts, t), widths
            else:
                return Reference(e.name, t), widths
            
        
        def infer_widths_s(s: Statement):
            widths: Dict[str, Width] = {}
            if isinstance(s, Connect):
                expr, widths = infer_widths_e(widths, s.expr)
                loc, widths = infer_widths_e(widths, s.loc)
                return Connect(loc, expr, s.info)


        def infer_widths_m(m: DefModule) -> DefModule:
            if hasattr(m, 'ports') and isinstance(m.ports, list):
                ports = list(map(lambda p: infer_widths_p(p), m.ports))
            if hasattr(m, 'body') and isinstance(m.body, Block) and isinstance(m.body.stmts, list):
                stmts = list(map(lambda s: infer_widths_s(s), m.body.stmts))
            
            return Module(m.name, ports, Block(stmts), m.typ, m.info)

        return Circuit(list(map(lambda m: infer_widths_m(m), c.modules)), c.main, c.info)