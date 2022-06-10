from pyhcl.ir.low_ir import *
from typing import List
from dataclasses import dataclass
from pyhcl.passes._pass import Pass

@dataclass
class RemoveAccess(Pass):
    def run(self, c: Circuit) -> Circuit:
        modules: List[Module] = []

        def remove_access(e: Expression, type: Type = None, name: str = None) -> Expression:
            if isinstance(e, Reference):
                return Reference(f"{e.name}{name}", type)
            elif isinstance(e, SubIndex):
                return remove_access(e.expr, type, f"_{e.value}")
            elif isinstance(e, SubField):
                return remove_access(e.expr, type, f"_{e.name}")
            else:
                return e

        def remove_access_e(e: Expression) -> Expression:
            if isinstance(e, (SubIndex, SubField)):
                return remove_access(e, e.typ)
            elif isinstance(e, ValidIf):
                return ValidIf(remove_access_e(e.cond), remove_access_e(e.value), e.typ)
            elif isinstance(e, Mux):
                return Mux(remove_access_e(e.cond), remove_access_e(e.tval), remove_access_e(e.fval), e.typ)
            elif isinstance(e, DoPrim):
                return DoPrim(e.op, [remove_access_e(arg) for arg in e.args], e.consts, e.typ)
            else:
                return e

        def remove_access_s(s: Statement) -> Statement:
            if isinstance(s, Block):
                stmts: List[Statement] = []
                for sx in s.stmts:
                    stmts.append(remove_access_s(sx))
                return Block(stmts)
            elif isinstance(s, Conditionally):
                return Conditionally(remove_access_e(s.pred), remove_access_s(s.conseq), remove_access_s(s.alt), s.info)
            elif isinstance(s, DefRegister):
                return DefRegister(s.name, s.typ, remove_access_e(s.clock), remove_access_e(s.reset), remove_access_e(s.init), s.info)
            elif isinstance(s, DefNode):
                return DefNode(s.name, remove_access_e(s.value), s.info)
            elif isinstance(s, DefMemPort):
                return DefMemPort(s.name, s.mem, remove_access_e(s.index), remove_access_e(s.clk), s.rw, s.info)
            elif isinstance(s, Connect):
                return Connect(remove_access_e(s.loc), remove_access_e(s.expr), s.info)
            else:
                return s

        def remove_access_m(m: DefModule) -> DefModule:
            if isinstance(m, Module):
                return Module(m.name, m.ports, remove_access_s(m.body), m.typ, m.info)
            else:
                return m

        for m in c.modules:
            modules.append(remove_access_m(m))
        return Circuit(modules, c.main, c.info)