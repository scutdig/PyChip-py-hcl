from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass
from pyhcl.passes.utils import AutoName

@dataclass
class ExpandWhens(Pass):
    def run(self, c: Circuit) -> Circuit:
        modules: List[DefModule] = []

        def auto_gen_name():
            return AutoName.auto_gen_name()

        def flatten(s: Statement) -> List[Statement]:
            new_stmts = []
            conseq, alt = s.conseq, s.alt
            if isinstance(conseq, EmptyStmt) or isinstance(alt, EmptyStmt):
                ...
            if isinstance(conseq, Conditionally):
                new_stmts += flatten(conseq)
            if isinstance(alt, Conditionally):
                new_stmts += flatten(alt)
            if isinstance(conseq, Block):
                for sx in conseq.stmts:
                    if isinstance(sx, Conditionally):
                        new_stmts = new_stmts + flatten(sx)
                    else:
                        new_stmts.append((s.pred, sx))
            if isinstance(alt, Block):
                for sx in alt.stmts:
                    if isinstance(sx, Conditionally):
                        new_stmts += flatten(sx)
                    else:
                        new_stmts.append((s.pred, sx))
            return new_stmts

        def expand_whens(stmt: Statement, stmts: List[Statement], reference: Dict[str, Expression]):
            if isinstance(stmt, Conditionally):
                flat_cond = flatten(stmt)
                for pred, sx in flat_cond:
                    if isinstance(sx, Connect):
                        name = auto_gen_name()
                        loc_name = sx.loc.verilog_serialize() if isinstance(sx.loc, SubIndex) else sx.loc.serialize()
                        loc = sx.loc if loc_name not in reference else reference[loc_name]
                        stmts.append(DefNode(name, Mux(pred, sx.expr, loc, sx.expr.typ)))
                        reference[loc_name] = Reference(name, sx.loc.typ)
                    else:
                        stmts.append(sx)
            else:
                stmts.append(stmt)

        def expand_whens_s(stmts: List[Statement]) -> List[Statement]:
            new_stmts = []
            reference: Dict[str, Expression] = {}
            for stmt in stmts:
                expand_whens(stmt, new_stmts, reference)
            for ref in reference:
                new_stmts.append(Connect(Reference(ref, reference[ref].typ), reference[ref]))
            return new_stmts

        def expand_whens_m(m: DefModule) -> DefModule:
            if isinstance(m, ExtModule):
                return m
            if not hasattr(m, 'body') or not isinstance(m.body, Block):
                return m
            if not hasattr(m.body, 'stmts') or not isinstance(m.body.stmts, list):
                return m
            
            return Module(m.name, m.ports, Block(expand_whens_s(m.body.stmts)), m.typ, m.info)

        for m in c.modules:
            modules.append(expand_whens_m(m))
        return Circuit(modules, c.main, c.info)