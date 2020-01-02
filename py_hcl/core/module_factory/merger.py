from typing import List

from .inherit_list.named_expr import NamedExprChain, \
    NamedExprNode, NamedExprHolder
from .inherit_list.stmt_holder import StmtChain, \
    StmtHolder, StmtNode


def merge_expr(modules: List[type],
               expr_holder: NamedExprHolder) -> NamedExprChain:
    expr_list = None
    for m in modules[::-1]:
        h = m.packed_module.named_expr_chain \
            .named_expr_chain_head.named_expr_holder
        expr_list = NamedExprNode(h, expr_list)

    expr_list = NamedExprNode(expr_holder, expr_list)
    return NamedExprChain(expr_list)


def merge_statement(modules: List[type],
                    stmt_holder: StmtHolder) -> StmtChain:
    stmt_list = None
    for m in modules[::-1]:
        h = m.packed_module.statement_chain \
            .stmt_chain_head.stmt_holder
        stmt_list = StmtNode(h, stmt_list)

    stmt_list = StmtNode(stmt_holder, stmt_list)
    return StmtChain(stmt_list)
