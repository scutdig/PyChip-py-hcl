from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass
from pyhcl.passes.utils import get_binary_width, AutoName

@dataclass
class ReplaceSubaccess(Pass):
    def run(self, c: Circuit) -> Circuit:
        modules: List[DefModule] = []

        def has_access(e: Expression) -> bool:
            if isinstance(e, SubAccess):
                return True
            elif isinstance(e, (SubField, SubIndex)):
                return has_access(e.expr)
            else:
                return False
        
        def get_ref_name(e: Expression) -> str:
            if isinstance(e, SubAccess):
                return get_ref_name(e.expr)
            elif isinstance(e, SubField):
                return get_ref_name(e.expr)
            elif isinstance(e, SubIndex):
                return get_ref_name(e.expr)
            elif isinstance(e, Reference):
                return e.name
        
        def auto_gen_name():
            return AutoName.auto_gen_name()
        
        def last_name():
            return AutoName.last_name()

        def replace_subaccess(e: Expression):
            cons: List[Expression] = []
            exps: List[Expression] = []
            if isinstance(e, SubAccess):
                xcons, xexps = replace_subaccess(e.expr)
                if len(cons) == 0 and len(xexps) == 0:
                    if isinstance(e.expr.typ, VectorType):
                        for i in range(e.expr.typ.size):
                            cons.append(DoPrim(Eq(), [e.index, UIntLiteral(i, IntWidth(get_binary_width(e.expr.typ.size)))], [], UIntType(IntWidth(1))))
                            exps.append(SubIndex("", e.expr, i, e.typ))
                    else:
                        exps.append(e)
                else:
                    if isinstance(e.expr.typ, VectorType):
                        for i in range(e.expr.typ.size):
                            for xcon in xcons:
                                cons.append(DoPrim(And(), [xcon, DoPrim(Eq(), [e.index, UIntLiteral(i, IntWidth(get_binary_width(e.expr.typ.size)))],
                                [], UIntType(IntWidth(1)))], [], UIntType(IntWidth(1))))
                            for xexp in xexps:
                                exps.append(SubIndex("", xexp, i, e.typ))
                    else:
                        cons, exps = xcons, xexps
            elif isinstance(e, SubField):
                xcons, xexps = replace_subaccess(e.expr)
                cons = xcons
                for xexp in xexps:
                    exps.append(SubField(xexp, e.name, e.typ))
            elif isinstance(e, SubIndex):
                xcons, xexps = replace_subaccess(e.expr)
                cons = xcons
                for xexp in xexps:
                    exps.append(SubIndex("", xexp, e.value, e.typ))
            
            return cons, exps

        def replace_subaccess_e(e: Expression, stmts: List[Statement], is_sink: bool = False, source: Expression = None) -> Expression:
            if isinstance(e, ValidIf):
                return ValidIf(replace_subaccess_e(e.cond, stmts), replace_subaccess_e(e.value, stmts), e.typ)
            elif isinstance(e, Mux):
                return Mux(replace_subaccess_e(e.cond, stmts), replace_subaccess_e(e.tval, stmts), replace_subaccess_e(e.fval, stmts), e.typ)
            elif isinstance(e, DoPrim):
                return DoPrim(e.op, [replace_subaccess_e(arg, stmts) for arg in e.args], e.consts, e.typ)
            elif isinstance(e, (SubAccess, SubField, SubIndex)) and has_access(e):
                if is_sink:
                    cons, exps = replace_subaccess(e)
                    gen_nodes: Dict[str, DefNode] = {}
                    connects: Dict[str, Connect] = {}
                    new_stats: List[Expression] = []
                    e_name = get_ref_name(e)
                    for stmt in stmts:
                        if isinstance(stmt, Connect) and get_ref_name(stmt.lexp) == e_name:
                            connects[e.verilog_serialize()] = stmt.expr
                        else:
                            new_stats.append(stmt)
                    stats = new_stats
                    for i in range(len(cons)):
                        stats.append(Connect(exps[i], Mux(cons[i], source, connects[exps[i].verilog_serialize()], e.typ)))
                    return
                else:
                    cons, exps = replace_subaccess(e)
                    gen_nodes: Dict[str, DefNode] = {}
                    for i in range(len(cons)):
                        if i == 0:
                            name = auto_gen_name()
                            gen_node = DefNode(name, ValidIf(cons[i], exps[i], e.typ))
                            stmts.append(gen_node)
                            gen_nodes[name] = gen_node
                        else:
                            last_node = gen_nodes[last_name()]
                            name = auto_gen_name()
                            gen_node = DefNode(name, Mux(cons[i], exps[i], Reference(last_node.name, last_node.value.typ), e.typ))
                            stmts.append(gen_node)
                            gen_nodes[name] = gen_node
                    return Reference(gen_nodes[last_name()].name, e.typ)
            else:
                return e

        def replace_subaccess_s(s: Statement) -> Statement:
            if isinstance(s, Block):
                stmts: List[Statement] = []
                for stmt in s.stmts:
                    if isinstance(stmt, Connect):
                        expr = replace_subaccess_e(stmt.expr, stmts)
                        loc = replace_subaccess_e(stmt.loc, stmts, True, expr)
                        if expr is not None:
                            stmts.append(Connect(loc, expr, stmt.info, stmt.blocking, stmt.bidirection, stmt.mem))
                        else:
                            stmts.append(stmt)
                    elif isinstance(stmt, DefNode):
                        stmts.append(DefNode(stmt.name, replace_subaccess_e(stmt.value, stmts), stmt.info))
                    elif isinstance(stmt, DefRegister):
                        stmts.append(DefRegister(stmt.name, stmt.typ, stmt.clock, stmt.reset, replace_subaccess_e(stmt.init), stmt.info))
                    elif isinstance(stmt, Conditionally):
                        stmts.append(replace_subaccess_s(stmt))
                    else:
                        stmts.append(stmt)
                return Block(stmts)
            elif isinstance(s, EmptyStmt):
                return EmptyStmt()
            elif isinstance(s, Conditionally):
                return Conditionally(s.pred, replace_subaccess_s(s.conseq), replace_subaccess_s(s.alt), s.info)
            else:
                return s

        def replace_subaccess_m(m: DefModule) -> DefModule:
            if isinstance(m, Module):
                return Module(m.name, m.ports, replace_subaccess_s(m.body), m.typ, m.info)
            else:
                return m

        for m in c.modules:
            modules.append(replace_subaccess_m(m))
        return Circuit(modules, c.main, c.info)