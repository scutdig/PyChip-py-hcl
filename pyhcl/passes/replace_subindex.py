from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass

@dataclass
class ReplaceSubindex(Pass):
    def run(self, c: Circuit) -> Circuit:
        modules: List[DefModule] = []

        def replace_subindex_e(e: Expression) -> Expression:
            if isinstance(e, SubIndex):
                return Reference(e.verilog_serialize(), e.typ)
            if isinstance(e, SubField):
                return Reference(e.verilog_serialize(), e.typ)
            if isinstance(e, SubAccess):
                return SubAccess(replace_subindex_e(e.expr), replace_subindex_e(e.index), e.typ)
            if isinstance(e, ValidIf):
                return ValidIf(e.cond, replace_subindex_e(e.value), e.typ)
            if isinstance(e, Mux):
                return Mux(e.cond, replace_subindex_e(e.tval), replace_subindex_e(e.fval), e.typ)
            if isinstance(e, DoPrim):
                return DoPrim(e.op, list(map(lambda ex: replace_subindex_e(ex), e.args)), e.consts, e.typ)
            return e

        def replace_subindex(stmt: Statement) -> Statement:
            if isinstance(stmt, Connect):
                return Connect(replace_subindex_e(stmt.loc), replace_subindex_e(stmt.expr),
                  stmt.info, stmt.blocking, stmt.bidirection, stmt.mem)
            elif isinstance(stmt, DefNode):
                return DefNode(stmt.name, replace_subindex_e(stmt.value), stmt.info)
            elif isinstance(stmt, DefRegister):
                return DefRegister(stmt.name, stmt.typ, replace_subindex_e(stmt.clock),
                  replace_subindex_e(stmt.reset), replace_subindex_e(stmt.init), stmt.info)
            elif isinstance(stmt, DefMemPort):
                return DefMemPort(stmt.name, stmt.mem, replace_subindex_e(stmt.index),
                  replace_subindex_e(stmt.clk), stmt.rw, stmt.info)
            elif isinstance(stmt, Conditionally):
                return Conditionally(replace_subindex_e(stmt.pred), replace_subindex(stmt.conseq),
                  replace_subindex(stmt.alt), stmt.info)
            elif isinstance(stmt, Block):
                return Block(replace_subindex_s(stmt.stmts))
            else:
                return stmt

        def replace_subindex_s(stmts: List[Statement]) -> List[Statement]:
            new_stmts = []
            for stmt in stmts:
                new_stmts.append(replace_subindex(stmt))
            return new_stmts

        def replace_subindex_m(m: DefModule) -> DefModule:
            if isinstance(m, ExtModule):
                return m
            if not hasattr(m, 'body') or not isinstance(m.body, Block):
                return m
            if not hasattr(m.body, 'stmts') or not isinstance(m.body.stmts, list):
                return m
            
            return Module(m.name, m.ports, Block(replace_subindex_s(m.body.stmts)), m.typ, m.info)

        for m in c.modules:
            modules.append(replace_subindex_m(m))
        return Circuit(modules, c.main, c.info)