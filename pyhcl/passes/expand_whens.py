from typing import List

from numpy import isin
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
        
        def last_name():
            return AutoName.last_name()

        def expand_whens(s: Statement, stmts: List[Statement], refs: Dict[str, List[Statement]], pred: Expression = None):
            if isinstance(s, Conditionally):
                expand_whens(s.conseq, stmts, refs, s.pred)
                expand_whens(s.alt, stmts, refs, DoPrim(Not(), [s.pred], [], s.pred.typ))
            elif isinstance(s, Block):
                for sx in s.stmts:
                    expand_whens(sx, stmts, refs, pred)
            elif isinstance(s, EmptyStmt):
                ...
            elif isinstance(s, Connect):
                if s.loc.serialize() not in refs:
                    refs[s.loc.serialize()] = []
                refs[s.loc.serialize()].append(Conditionally(pred, Block([s]), EmptyStmt()))
            else:
                stmts.append(s)

        def expand_whens_s(ss: List[Statement]) -> List[Statement]:
            stmts: List[Statement] = []
            refs: Dict[str, List[Statement]] = {}
            for sx in ss:
                if isinstance(sx, Conditionally):
                    expand_whens(sx, stmts, refs)
                else:
                    stmts.append(sx)
            for sx in refs.values():
                if len(sx) <= 1:
                    sxx = sx.pop()
                    con = sxx.conseq.stmts.pop()
                    stmts.append(Connect(con.loc, ValidIf(sxx.pred, con.expr, con.expr.typ)))
                else:
                    sxx = sx.pop()
                    con = sxx.conseq.stmts.pop()
                    stmts.append(DefNode(auto_gen_name(), ValidIf(sxx.pred, con.expr, con.expr.typ)))
                    while len(sx) > 1:
                        sxx = sx.pop()
                        con = sxx.conseq.stmts.pop()
                        stmts.append(DefNode(auto_gen_name(), Mux(sxx.pred, con.expr, Reference(AutoName.last_name(), con.expr.typ), con.expr.typ)))
                    sxx = sx.pop()
                    con = sxx.conseq.stmts.pop()
                    stmts.append(Connect(con.loc, Mux(sxx.pred, con.expr, Reference(last_name(), con.expr.typ), con.expr.typ)))
            return stmts

        def expand_whens_m(m: DefModule) -> DefModule:
            if isinstance(m, Module):
                return Module(m.name, m.ports, Block(expand_whens_s(m.body.stmts)), m.typ, m.info)
            else:
                return m

        for m in c.modules:
            modules.append(expand_whens_m(m))
        return Circuit(modules, c.main, c.info)