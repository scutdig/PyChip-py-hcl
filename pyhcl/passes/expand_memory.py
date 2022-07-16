from typing import List, Dict
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass
from pyhcl.passes.utils import get_binary_width

DEFAULT_READ_LATENCY = 0
DEFAULT_WRITE_LATENCY = 1

@dataclass
class ExpandMemory(Pass):
    def run(self, c: Circuit):

        def get_mem_ports(stmts: List[Statement], writes: Dict[str, List[Statement]], reads: Dict[str, List[Statement]]):
            for stmt in stmts:
                if isinstance(stmt, DefMemPort):
                    if stmt.rw is True:
                        if stmt.mem.name in reads:
                            reads[stmt.mem.name] = reads[stmt.mem.name] + [stmt.name]
                        else:
                            reads[stmt.mem.name] = [stmt.name]
                    else:
                        if stmt.mem.name in writes:
                            writes[stmt.mem.name] = writes[stmt.mem.name] + [stmt.name]
                        else:
                            writes[stmt.mem.name] = [stmt.name]
        def expand_mem_port(stmts: List[Statement], target: Statement):
            addr_width = IntWidth(get_binary_width(target.mem.typ.size))
            # addr
            stmts.append(Connect(
                SubField(SubField(Reference(target.mem.name, UIntType(addr_width)),target.name, UIntType(addr_width)), 'addr', UIntType(addr_width)),
                UIntLiteral(target.index.value, addr_width)))
            # en
            stmts.append(Connect(
                SubField(SubField(Reference(target.mem.name, UIntType(IntWidth(1))),target.name, UIntType(IntWidth(1))), 'en', UIntType(IntWidth(1))),
                UIntLiteral(1, IntWidth(1))))
            # clk
            stmts.append(Connect(
                SubField(SubField(Reference(target.mem.name, ClockType()),target.name, ClockType()), 'clk', ClockType()),
                target.clk))
            # mask
            if target.rw is False:
                stmts.append(Connect(
                    SubField(SubField(Reference(target.mem.name, UIntType(IntWidth(1))),target.name, UIntType(IntWidth(1))), 'mask', UIntType(IntWidth(1))),
                    UIntLiteral(1, IntWidth(1))))
        
        def expand_memory_e(s: Statement, ports: Dict[str, Statement]) -> Statement:
            loc, expr = s.loc, s.expr
            if isinstance(loc, Reference) and loc.name in ports:
                loc = SubField(SubField(Reference(ports[loc.name].mem.name, loc.typ), loc.name, loc.typ), 'data', loc.typ)
            elif isinstance(expr, Reference) and expr.name in ports:
                expr = SubField(SubField(Reference(ports[expr.name].mem.name, expr.typ), expr.name, expr.typ), 'data', expr.typ)
            return Connect(loc, expr, s.info, s.blocking, s.bidirection, s.mem)

        def expand_memory_s(stmts: List[Statement]) -> List[Statement]:
            new_stmts: List[Statement] = []
            writes: Dict[str, List[Statement]] = {}
            reads: Dict[str, List[Statement]] = {}
            ports: Dict[str, List[Statement]] = {}
            get_mem_ports(stmts, writes, reads)
            for stmt in stmts:
                if isinstance(stmt, DefMemory):
                    new_stmts.append(WDefMemory(
                        stmt.name,
                        stmt.memType,
                        stmt.memType.typ,
                        stmt.memType.size,
                        DEFAULT_READ_LATENCY,
                        DEFAULT_WRITE_LATENCY,
                        reads[stmt.name], 
                        writes[stmt.name]))
                elif isinstance(stmt, DefMemPort):
                    expand_mem_port(new_stmts, stmt)
                    ports[stmt.name] = stmt
                elif isinstance(stmt, Connect):
                    new_stmts.append(expand_memory_e(stmt, ports))
                else:
                    new_stmts.append(stmt)
            return new_stmts

        def expand_memory_m(m: DefModule) -> DefModule:
            return Module(
                m.name,
                m.ports,
                Block(expand_memory_s(m.body.stmts)),
                m.typ,
                m.info
            )

        new_modules = []
        for m in c.modules:
            if isinstance(m, Module):
                new_modules.append(expand_memory_m(m))
            else:
                new_modules.append(m)
        
        return Circuit(new_modules, c.main, c.info)