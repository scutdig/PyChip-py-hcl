from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass
from pyhcl.passes.utils import get_binary_width

@dataclass
class ReplaceSubaccess(Pass):
    endwith: int = -1

    def run(self, c: Circuit) -> Circuit:
        modules: List[DefModule] = []

        def auto_gen_name():
            self.endwith += 1
            return f'_GEN_{self.endwith}'

        def get_groud_type(t: Type) -> Type:
            if isinstance(t, VectorType):
                return get_groud_type(t.typ)
            else:
                return t

        def get_type(e: Expression) -> Type:
            if isinstance(e, SubAccess):
                return get_type(e.expr)
            else:
                return e.typ

        def replace_subaccess_e(e: Expression, t: Type):
            exprs = []
            new_exprs = []
            index = []
            new_index = []
            if type(e.expr) == SubAccess:
                exprs, index = replace_subaccess_e(e.expr, t.typ)
            if type(e.expr) == Reference:
                for i in range(t.size):
                    new_exprs.append(DoPrim(Eq(), [UIntLiteral(i, IntWidth(get_binary_width(i))), e.index], [], UIntType(1)))
                    new_index.append(SubIndex('', e.expr, i, t))
            else:
                for i in range(t.size):
                    for expr in exprs:
                        new_exprs.append(DoPrim(And(), [DoPrim(Eq(), [UIntLiteral(i, IntWidth(get_binary_width(i))), e.index],
                          [], UIntType(1)), expr], [], UIntType(1)))
                    for ind in index:
                        new_index.append(SubIndex('', ind, i, t))
                
            return new_exprs, new_index       

        def replace_subaccess(target_s: Statement, stmts: List[Statement]):
            nodes = []
            exprs, index = replace_subaccess_e(target_s.expr, get_type(target_s.expr))
            if len(exprs) == len(index):
                for i in range(len(exprs)):
                    if i == 0:
                        node = DefNode(auto_gen_name(),
                          ValidIf(exprs[i], index[i], get_groud_type(get_type(target_s.expr))))
                        stmts.append(node)
                        nodes.append(node)
                    else:
                        node = DefNode(auto_gen_name(), Mux(exprs[i], index[i],
                        Reference(nodes[-1].name, nodes[-1].value.typ), get_groud_type(get_type(target_s.expr))))
                        stmts.append(node)
                        nodes.append(node)
                stmts.append(Connect(target_s.loc, Reference(nodes[-1].name, nodes[-1].value.typ)))

        def replace_subaccess_s(stmts: List[Statement]) -> List[Statement]:
            new_stmts = []
            for stmt in stmts:
                if isinstance(stmt, Connect) and isinstance(stmt.expr, SubAccess):
                    replace_subaccess(stmt, new_stmts)
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