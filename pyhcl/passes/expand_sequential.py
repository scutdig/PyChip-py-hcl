from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from typing import List, Dict
from dataclasses import dataclass
from pyhcl.passes._pass import Pass

@dataclass
class ExpandSequential(Pass):

    def run(self, c: Circuit):
        modules: List[Module] = []
        blocks: List[Statement] = []
        block_map: Dict[str, List[Statement]] = {}
        clock_map: Dict[str, Expression] = {}

        def get_ref_name(e: Expression) -> str:
            if isinstance(e, SubAccess):
                return get_ref_name(e.expr)
            elif isinstance(e, SubField):
                return get_ref_name(e.expr)
            elif isinstance(e, SubIndex):
                return get_ref_name(e.expr)
            elif isinstance(e, Reference):
                return e.name

        def expand_sequential_s(s: Statement, stmts: List[Statement], reg_map: Dict[str, DefRegister]):
            if isinstance(s, Conditionally):
                conseq_seq_map, conseq_com = expand_sequential_s(s.conseq, stmts, reg_map)
                alt_seq_map, alt_com = expand_sequential_s(s.alt, stmts, reg_map)
                for k in conseq_seq_map:
                    if k not in alt_seq_map:
                        alt_seq_map[k] = EmptyStmt()
                com = Conditionally(s.pred, conseq_com, alt_com, s.info)
                if isinstance(conseq_com, EmptyStmt):
                    if isinstance(alt_com, EmptyStmt):
                        com = EmptyStmt()
                    else:
                        com = Conditionally(DoPrim(Not(), [s.pred], [], s.pred.typ))
                return {k: Conditionally(s.pred, v, alt_seq_map[k], s.info) for k, v in conseq_seq_map.items()}, com
            elif isinstance(s, Block):
                com_stmts: List[Statement] = []
                seq_stmts_map: Dict[str, List[Statement]] = {}
                for sx in s.stmts:
                    if isinstance(sx, Connect) and get_ref_name(sx.loc) in reg_map:
                        reg = reg_map[get_ref_name(sx.loc)]
                        if reg.clock.verilog_serialize() not in clock_map:
                            clock_map[reg.clock.verilog_serialize()] = reg.clock
                        if reg.clock.verilog_serialize() not in seq_stmts_map:
                            seq_stmts_map[reg.clock.verilog_serialize()] = []
                        seq_stmts_map[reg.clock.verilog_serialize()].append(Connect(sx.loc, sx.expr, sx.info, False, sx.bidirection, sx.mem))
                    elif isinstance(sx, Connect) and get_ref_name(sx.loc) not in reg_map:
                        com_stmts.append(sx)
                    elif isinstance(sx, Conditionally):
                        seq_when_map, com_when = expand_sequential_s(sx, stmts, reg_map)
                        for k in seq_when_map:
                            if k not in seq_stmts_map:
                                seq_stmts_map[k] = []
                            seq_stmts_map[k].append(seq_when_map[k])
                        com_stmts.append(com_when)
                    else:
                        stmts.append(sx)
                return {k: Block(v) if len(v) > 0 else EmptyStmt() for k, v in seq_stmts_map.items()}, \
                    Block(com_stmts) if len(com_stmts) > 0 else EmptyStmt()
            else:
                return {}, s

        def expand_sequential(stmts: List[Statement]) -> List[Statement]:
            reg_map: Dict[str, DefRegister] = {sx.name: sx for sx in stmts if isinstance(sx, DefRegister)}
            mem_map: Dict[str, DefMemPort] = {sx.name: sx for sx in stmts if isinstance(sx, DefMemPort)}
            new_stmts: List[Statement] = []
            for stmt in stmts:
                if isinstance(stmt, Conditionally):
                    seq_map, com = expand_sequential_s(stmt, new_stmts, reg_map)
                    if not isinstance(com, EmptyStmt):
                        new_stmts.append(com)
                    for k in seq_map:
                        if k not in block_map:
                            block_map[k] = []
                        if not isinstance(seq_map[k], EmptyStmt):
                            block_map[k].append(seq_map[k])
                else:
                    new_stmts.append(stmt)
            reset_map: Dict[str, List[Statement]] = {}
            reset_sign_map: Dict[str, List[Expression]] = {}
            for reg_name in reg_map:
                reg: DefRegister = reg_map[reg_name]
                if reg.init is not None:
                    if reg.clock.verilog_serialize() not in reset_map:
                        reset_map[reg.clock.verilog_serialize()] = []
                    reset_map[reg.clock.verilog_serialize()].append(Connect(Reference(reg.name, reg.typ), reg.init, reg.info, False))
                    if reg.clock.verilog_serialize not in reset_sign_map:
                        reset_sign_map[reg.clock.verilog_serialize()] = []
                    reset_sign_map[reg.clock.verilog_serialize()].append(reg.reset)
            for k in reset_map:
                if len(reset_map[k]) > 0:
                    for rs in reset_sign_map[k]:
                        block_map[k].append(Conditionally(rs, Block(reset_map[k]), EmptyStmt()))
            for k in mem_map:
                mem: Reference = mem_map[k].mem
                sig = DoPrim(And(), [Reference(f"{mem.name}_{k}_en", UIntType(IntWidth(1))),
                Reference(f"{mem.name}_{k}_mask", UIntType(IntWidth(1)))], [], UIntType(IntWidth(1)))
                con = Connect(SubAccess(mem, Reference(f"{mem.name}_{k}_addr", mem_map[k].index.typ), mem.typ),
                Reference(f"{mem.name}_{k}_data", mem.typ),mem_map[k].info, False)
                if mem_map[k].rw is False:
                    if mem_map[k].clk.verilog_serialize() not in block_map:
                        block_map[mem_map[k].clk.verilog_serialize()] = []
                    if mem_map[k].clk.verilog_serialize() not in clock_map:
                        clock_map[mem_map[k].clk.verilog_serialize()] = mem_map[k].clk
                    block_map[mem_map[k].clk.verilog_serialize()].append(Conditionally(sig, Block([con]), EmptyStmt()))
            for k in block_map:
                new_stmts.append(AlwaysBlock(block_map[k], clock_map[k]))
            return new_stmts      

        def expand_sequential_m(m: DefModule) -> DefModule:
            if isinstance(m, Module):
                return Module(m.name, m.ports, Block(expand_sequential(m.body.stmts)), m.typ)
            else:
                return m

        for m in c.modules:
            modules.append(expand_sequential_m(m))
        return Circuit(modules, c.main, c.info)