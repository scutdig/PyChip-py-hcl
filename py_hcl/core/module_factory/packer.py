from py_hcl.core.module.packed_module import PackedModule
from py_hcl.core.module_factory.inherit_list.named_expr import NamedExprHolder
from py_hcl.core.module_factory.inherit_list.stmt_holder import StmtHolder
from py_hcl.core.stmt_factory.trapper import StatementTrapper
from py_hcl.core.utils import module_inherit_mro
from . import extractor
from . import merger
from ..stmt import ClusterStatement, ConditionStatement
from ..stmt_factory.scope import ScopeType


def pack(bases, dct, name) -> PackedModule:
    raw_expr = extractor.extract(dct)
    raw_statement = normalize_conditional_branch(StatementTrapper.trap())

    named_expr_chain, statement_chain = \
        handle_inherit(bases, raw_expr, raw_statement, name)

    res = PackedModule(name, named_expr_chain, statement_chain)
    return res


def handle_inherit(bases, named_expression, top_statement, name):
    modules = module_inherit_mro(bases)

    named_expr_chain = \
        merger.merge_expr(modules, NamedExprHolder(name, named_expression))

    statement_chain = \
        merger.merge_statement(modules, StmtHolder(name, top_statement))

    return named_expr_chain, statement_chain


def normalize_conditional_branch(cluster_statement: ClusterStatement):
    new_statements = []

    waiting_when = None
    for s in cluster_statement.statements:
        if s.stmt_class == 'line':
            new_statements.append(s)
            continue

        normalized = normalize_conditional_branch(s)
        if s.scope_info.scope_type == ScopeType.WHEN:
            cond_id = normalized.scope_info.tag_object.cond_expr_id
            cs = ConditionStatement(cond_id, normalized.statements, None)
            new_statements.append(cs)
            waiting_when = cs

        elif s.scope_info.scope_type == ScopeType.ELSE_WHEN:
            cond_id = normalized.scope_info.tag_object.cond_expr_id
            cs = ConditionStatement(cond_id, normalized.statements, None)
            waiting_when.alt_stmts = [cs]
            waiting_when = cs

        else:
            waiting_when.alt_stmts = normalized.statements

    cluster_statement.statements = new_statements
    return cluster_statement
