from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass
from pyhcl.passes.utils import get_binary_width, AutoName

@dataclass
class ReplaceSubaccess(Pass):
    # endwith: int = -1

    def run(self, c: Circuit) -> Circuit:
        modules: List[DefModule] = []

        # def auto_gen_name():
        #     self.endwith += 1
        #     return f'_GEN_{self.endwith}'
        
        def auto_gen_name():
            return AutoName.auto_gen_name()

        def get_groud_type(t: Type) -> Type:
            if isinstance(t, VectorType):
                return get_groud_type(t.typ)
            else:
                return t

        def get_type(e: Expression) -> Type:
            if isinstance(e, (SubAccess, SubIndex)):
                return get_type(e.expr)
            else:
                return e.typ

        def replace_subaccess_e(e: Expression):
            exprs = []
            index = []
            size = 0
            if isinstance(e, SubAccess):
                subexprs, subindex, size = replace_subaccess_e(e.expr)
                for n in range(size):
                    if len(subexprs) == 0:
                        exprs.append(DoPrim(Eq(), [e.index, UIntLiteral(n, IntWidth(get_binary_width(n)))], [], UIntType(1)))
                    else:
                        for expr in subexprs:
                            exprs.append(DoPrim(And(), [DoPrim(Eq(), [e.index, UIntLiteral(n, IntWidth(get_binary_width(n)))],
                                [], UIntType(1)), expr], [], UIntType(1)))
                    for ind in subindex:
                        index.append(SubIndex('', ind, n, e.typ))
                size = e.typ.size if hasattr(e.typ, 'size') else 0
            if isinstance(e, SubIndex):
                subexprs, subindex, size = replace_subaccess_e(e.expr)
                if len(subexprs) == 0:
                    index.append(e)
                else:
                    exprs = subexprs
                    index = list(map(lambda i: SubIndex(e.name, i, e.value, e.typ), subindex))
                size = e.typ.size if hasattr(e.typ, 'size') else 0
            elif isinstance(e, (Reference, SubField)):
                index.append(e)
                size = e.typ.size if hasattr(e.typ, 'size') else 0
                
            return exprs, index, size      

        def replace_subaccess(target_e: Expression, stmts: List[Statement]) -> Expression:
            if isinstance(target_e, Mux):
                return Mux(target_e.cond, replace_subaccess(target_e.tval, stmts), replace_subaccess(target_e.fval, stmts), target_e.typ)
            if isinstance(target_e, ValidIf):
                return ValidIf(target_e.cond, replace_subaccess(target_e.value, stmts), target_e.typ)
            if isinstance(target_e, DoPrim):
                return DoPrim(target_e.op, list(map(lambda arg: replace_subaccess(arg, stmts), target_e.args)), target_e.consts, target_e.typ)
            nodes = []
            exprs, index, _ = replace_subaccess_e(target_e)
            if len(exprs) > 0 and len(index) > 0 and len(exprs) == len(index):
                for i in range(len(exprs)):
                    if i == 0:
                        node = DefNode(auto_gen_name(),
                          ValidIf(exprs[i], index[i], get_groud_type(get_type(target_e))))
                        stmts.append(node)
                        nodes.append(node)
                    else:
                        node = DefNode(auto_gen_name(), Mux(exprs[i], index[i],
                        Reference(nodes[-1].name, nodes[-1].value.typ), get_groud_type(get_type(target_e))))
                        stmts.append(node)
                        nodes.append(node)
                return Reference(nodes[-1].name, nodes[-1].value.typ)
            return target_e

        def replace_subaccess_s(stmts: List[Statement]) -> List[Statement]:
            new_stmts = []
            for stmt in stmts:
                if isinstance(stmt, Connect):
                    new_stmts.append(Connect(stmt.loc, replace_subaccess(stmt.expr, new_stmts)))
                elif isinstance(stmt, Conditionally):
                    conseq = Block(replace_subaccess_s(stmt.conseq.stmts))
                    alt = EmptyStmt() if isinstance(stmt.alt, EmptyStmt) else Block(replace_subaccess_s(stmt.alt.stmts))
                    new_stmts.append(Conditionally(stmt.pred, conseq, alt, stmt.info))
                elif isinstance(stmt, DefNode):
                    new_stmts.append(DefNode(stmt.name, replace_subaccess(stmt.value, new_stmts), stmt.info))
                else:
                    new_stmts.append(stmt)
            return new_stmts

        def replace_subaccess_m(m: DefModule) -> DefModule:
            if isinstance(m, ExtModule):
                return m
            if not hasattr(m, 'body') or not isinstance(m.body, Block):
                return m
            if not hasattr(m.body, 'stmts') or not isinstance(m.body.stmts, list):
                return m
            
            return Module(m.name, m.ports, Block(replace_subaccess_s(m.body.stmts)), m.typ, m.info)

        for m in c.modules:
            modules.append(replace_subaccess_m(m))
        return Circuit(modules, c.main, c.info)