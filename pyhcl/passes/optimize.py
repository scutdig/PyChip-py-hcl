from typing import List, Dict
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass

@dataclass
class Optimize(Pass):
    def run(self, c: Circuit):
        def get_name(e: Expression) -> str:
            if isinstance(e, (SubField, SubIndex, SubAccess)):
                return get_name(e.expr)
            else:
                return e.name

        def optimize_s(stmts: List[Statement]) -> List[Statement]:
            defwires: Dict[str, Statement] = {}
            connects: Dict[str, Statement] = {}
            nodes: Dict[str, Statement] = {}
            new_stmts: List[Statement] = []
            for stmt in stmts:
                if isinstance(stmt, DefWire):
                    defwires[stmt.name] = stmt
                if isinstance(stmt, Connect):
                    connects[get_name(stmt.loc)] = stmt

            
            for defwire in defwires.keys():
                if defwire in connects:
                    nodes[defwire] = DefNode(defwire, connects[defwire].expr)

            for stmt in stmts:
                if isinstance(stmt, DefWire) and stmt.name in nodes:
                    new_stmts.append(nodes[stmt.name])
                elif isinstance(stmt, Connect) and get_name(stmt.loc) in nodes:
                    ...
                else:
                    new_stmts.append(stmt)

            return new_stmts

        def optimize_m(m: DefModule) -> DefModule:
            return Module(
                m.name,
                m.ports,
                Block(optimize_s(m.body.stmts)),
                m.typ,
                m.info
            )

        new_modules = []
        for m in c.modules:
            if isinstance(m, Module):
                new_modules.append(optimize_m(m))
            else:
                new_modules.append(m)
        
        return Circuit(new_modules, c.main, c.info)