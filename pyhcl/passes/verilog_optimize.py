from dataclasses import dataclass
from pyhcl.ir.low_ir import *
from pyhcl.passes._pass import Pass
from typing import List, Dict
from pyhcl.passes.utils import AutoName

@dataclass
class VerilogOptimize(Pass):
    def run(self, c: Circuit):
        modules: List[DefModule] = []

        def auto_gen_node(s):
            return isinstance(s, DefNode) and s.name.startswith("_T")
        
        def get_name(e: Expression) -> str:
            if isinstance(e, (SubAccess, SubField, SubIndex)):
                return get_name(e.expr)
            elif isinstance(e, Reference):
                return e.verilog_serialize()

        def verilog_optimize_e(expr: Expression, node_map: Dict[str, Statement], filter_nodes: set, stmts: List[Statement]) -> Expression:
            if isinstance(expr, (UIntLiteral, SIntLiteral)):
                return expr
            elif isinstance(expr, Reference):
                en = get_name(expr)
                if en in node_map:
                    filter_nodes.add(en)
                    return verilog_optimize_e(node_map[en].value, node_map, filter_nodes, stmts)
                else:
                    return expr
            elif isinstance(expr, (SubField, SubIndex, SubAccess)):
                return expr
            elif isinstance(expr, Mux):
                return Mux(
                    verilog_optimize_e(expr.cond, node_map, filter_nodes, stmts),
                    verilog_optimize_e(expr.tval, node_map, filter_nodes, stmts),
                    verilog_optimize_e(expr.fval, node_map, filter_nodes, stmts), expr.typ)
            elif isinstance(expr, ValidIf):
                return ValidIf(
                    verilog_optimize_e(expr.cond, node_map, filter_nodes, stmts),
                    verilog_optimize_e(expr.value, node_map, filter_nodes, stmts), expr.typ)
            elif isinstance(expr, DoPrim):
                args = list(map(lambda arg: verilog_optimize_e(arg, node_map, filter_nodes, stmts), expr.args))
                if isinstance(expr.op, Bits) and isinstance(args[0], DoPrim):
                    name = AutoName.auto_gen_name()
                    stmts.append(DefNode(name, args[0]))
                    args = [Reference(name, args[0].typ)]
                return DoPrim(expr.op, args, expr.consts, expr.typ)
            else:
                return expr

        def verilog_optimize_s(stmt: Statement, node_map: Dict[str, Statement], filter_nodes: set, stmts: List[Statement] = None) -> Statement:
            if isinstance(stmt, Block):
                node_map = {**node_map ,**{sx.name: sx for sx in stmt.stmts if auto_gen_node(sx)}}
                cat_stmts = []
                for sx in stmt.stmts:
                    if isinstance(sx, Connect):
                        cat_stmts.append(Connect(verilog_optimize_e(sx.loc, node_map, filter_nodes, cat_stmts),
                        verilog_optimize_e(sx.expr, node_map, filter_nodes, cat_stmts), sx.info, sx.blocking, sx.bidirection, sx.mem))
                    elif isinstance(sx, DefNode):
                        cat_stmts.append(DefNode(sx.name, verilog_optimize_e(sx.value, node_map, filter_nodes, cat_stmts), sx.info))
                    elif isinstance(sx, Conditionally):
                        cat_stmts.append(Conditionally(verilog_optimize_e(sx.pred, node_map, filter_nodes, cat_stmts), verilog_optimize_s(sx.conseq, node_map, filter_nodes, cat_stmts),
                        verilog_optimize_s(sx.alt, node_map, filter_nodes, cat_stmts), sx.info))
                    else:
                        cat_stmts.append(sx)
                cat_stmts = [sx for sx in cat_stmts if not (isinstance(sx, DefNode) and sx.name in filter_nodes)]
                return Block(cat_stmts)                    
            elif isinstance(stmt, Conditionally):
                return Conditionally(verilog_optimize_e(stmt.pred, node_map, filter_nodes, stmts), verilog_optimize_s(stmt.conseq, node_map, filter_nodes, stmts), 
                verilog_optimize_s(stmt.alt, node_map, filter_nodes, stmts), stmt.info)
            else:
                return stmt


        def verilog_optimize_m(m: DefModule) -> DefModule:
            node_map: Dict[str, DefNode] = {}
            filter_nodes: set = set()
            if isinstance(m, Module):
                return Module(m.name, m.ports, verilog_optimize_s(m.body, node_map, filter_nodes), m.typ, m.info)
            else:
                return m       

        for m in c.modules:
            modules.append(verilog_optimize_m(m))
        return Circuit(modules, c.main, c.info)