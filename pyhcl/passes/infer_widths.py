from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass
from pyhcl.passes.wir import *

class InferWidths(Pass):
    @staticmethod
    def run(c: Circuit):
        def infer_widths_t(widths: Dict[str, Width], name: str, t: Type) -> tuple[Type, List[Width]]:
            if isinstance(t, BundleType):
                bs = list(map(lambda f: infer_widths_t(widths, name, f.typ), t.fields))
                bs = [b for b in bs if b is not None].pop()
                t, widths = bs[0], bs[1]
            
            elif isinstance(t, MemoryType):
                return infer_widths_t(widths, name, t.typ)

            elif isinstance(t, VectorType):
                return infer_widths_t(widths, name, t.typ)

            elif isinstance(t, UIntType):
                if isinstance(t.width, UnknownWidth):
                    return UIntType(widths.values().pop()), widths.clear()
                else:
                    widths[name] = t.width
            elif isinstance(t, SIntType):
                if isinstance(t.width, UnknownWidth):
                    return SIntType(widths.values().pop()), widths.clear()
                else:
                    widths[name] = t.width
            
            elif isinstance(t, ClockType):
                if isinstance(t.width, UnknownWidth):
                    return ClockType(widths.values().pop()), widths.clear()
                else:
                    widths[name] = t.width
            
            elif isinstance(t, ResetType):
                if isinstance(t.width, UnknownWidth):
                    return ResetType(widths.values().pop()), widths.clear()
                else:
                    widths[name] = t.width
            
            elif isinstance(t, AsyncResetType):
                if isinstance(t.width, UnknownWidth):
                    return AsyncResetType(widths.values().pop()), widths.clear()
                else:
                    widths[name] = t.width

            return t, widths
        
        def infer_widths_p(widths: Dict[str, Width], p: Port):
            # TODO: infer widths in port
            return p

        def infer_widths_e(widths: Dict[str, Width], e: Expression):
            if isinstance(e, UIntLiteral):
                return e, widths
            elif isinstance(e, SIntLiteral):
                return e, widths
            elif isinstance(e, SubField):
                t, widths = infer_widths_t(widths, e.name, e.typ)
                return SubField(e.expr, e.name, t), widths
            elif isinstance(e, SubAccess):
                t, widths = infer_widths_t(widths, '', e.typ)
                return SubAccess(e.expr, e.index, t), widths
            elif isinstance(e, SubIndex):
                t, widths = infer_widths_t(widths, e.name, e.typ)
                return SubIndex(e.name, e.expr, e.value, t), widths
            elif isinstance(e, DoPrim):
                t, widths = infer_widths_t(widths, '', e.typ)
                return DoPrim(e.op, e.args, e.consts, t), widths
            elif isinstance(e, Mux):
                t, widths = infer_widths_t(widths, '', e.typ)
                return Mux(e.cond, e.tval, e.fval, t), widths
            elif isinstance(e, ValidIf):
                t, widths = infer_widths_t(widths, '', e.typ)
                return Mux(e.cond, e.value, t), widths
            else:
                t, widths = infer_widths_t(widths, e.name, e.typ)
                return Reference(e.name, t), widths
            
        
        def infer_widths_s(widths: Dict[str, Width], s: Statement):
            if isinstance(s, Connect):
                expr, widths = infer_widths_e(widths, s.expr)
                loc, widths = infer_widths_e(widths, s.loc)
                return Connect(loc, expr, s.info)
            return s


        def infer_widths_m(m: DefModule) -> DefModule:
            if isinstance(m, ExtModule):
                return m
            widths: Dict[str, Width] = {}
            ports = None
            stmts = None
            if hasattr(m, 'ports') and isinstance(m.ports, list):
                ports = list(map(lambda p: infer_widths_p(widths, p), m.ports))
            if hasattr(m, 'body') and isinstance(m.body, Block):
                if hasattr(m.body, 'stmts') and isinstance(m.body.stmts, list):
                    stmts = list(map(lambda s: infer_widths_s(widths, s), m.body.stmts))
            
            return Module(m.name, ports, Block(stmts), m.typ, m.info)

        return Circuit(list(map(lambda m: infer_widths_m(m), c.modules)), c.main, c.info)