from py_hcl.core.module.packed_module import PackedModule
from py_hcl.core.module_factory.inherit_list.named_expr import NamedExprHolder
from py_hcl.core.module_factory.inherit_list.stmt_holder import StmtHolder
from py_hcl.core.stmt_factory.trapper import StatementTrapper
from py_hcl.core.utils import module_inherit_mro
from . import extractor
from . import merger


def pack(bases, dct, name) -> PackedModule:
    raw_expr = extractor.extract(dct)
    raw_scope = StatementTrapper.trap()

    named_expr_chain, statement_chain = \
        handle_inherit(bases, raw_expr, raw_scope, name)

    res = PackedModule(name, named_expr_chain, statement_chain)
    return res


def handle_inherit(bases, named_expression, top_statement, name):
    modules = module_inherit_mro(bases)

    named_expr_chain = \
        merger.merge_expr(modules, NamedExprHolder(name, named_expression))

    statement_chain = \
        merger.merge_statement(modules, StmtHolder(name, top_statement))

    return named_expr_chain, statement_chain
