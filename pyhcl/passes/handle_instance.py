from dataclasses import dataclass
from typing import List, Dict
from pyhcl.ir.low_ir import *
from pyhcl.passes._pass import Pass

@dataclass
class HandleInstance(Pass):
    def run(self, c: Circuit) -> Circuit:
        modules: List[DefModule] = []
        refs: Dict[str, List[Port]] = {m.name: m.ports for m in c.modules}

        def handle_instance_s(s: Statement):
            if isinstance(s, Conditionally):
                return Conditionally(s.pred, handle_instance_s(s.conseq), handle_instance_s(s.alt), s.info)
            elif isinstance(s, Block):
                return Block([handle_instance_s(sx) for sx in s.stmts])
            elif isinstance(s, DefInstance):
                if s.module in refs:
                    return DefInstance(s.name, s.module, refs[s.module], s.info)
                else:
                    return s
            else:
                return s

        def handle_instance_m(m: DefModule):
            if isinstance(m, Module):
                return Module(m.name, m.ports, handle_instance_s(m.body), m.typ, m.info)
            else:
                return m

        for m in c.modules:
            modules.append(handle_instance_m(m))
        return Circuit(modules, c.main, c.info)