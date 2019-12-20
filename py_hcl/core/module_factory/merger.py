from typing import List

from py_hcl.core.module_factory.inherit_list.named_expr import NamedExprList, \
    NamedExprNode, NamedExprHolder
from py_hcl.core.module_factory.inherit_list.stmt_holder import StmtList, \
    StmtHolder, StmtNode


def merge_expr(modules: List[type],
               expr_holder: NamedExprHolder) -> NamedExprList:
    expr_list = None
    for m in modules[::-1]:
        h = m.packed_module.named_expr_list \
            .named_expr_list_head.named_expr_holder
        expr_list = NamedExprNode(h, expr_list)

    expr_list = NamedExprNode(expr_holder, expr_list)
    return NamedExprList(expr_list)


def merge_statement(modules: List[type],
                    stmt_holder: StmtHolder) -> StmtList:
    stmt_list = None
    for m in modules[::-1]:
        h = m.packed_module.statement_list \
            .stmt_list_head.stmt_holder
        stmt_list = StmtNode(h, stmt_list)

    stmt_list = StmtNode(stmt_holder, stmt_list)
    return StmtList(stmt_list)
