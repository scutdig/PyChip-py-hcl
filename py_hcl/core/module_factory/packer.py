from py_hcl.core.module_factory.inherit_list.named_expr import NamedExprHolder
from py_hcl.core.module_factory.inherit_list.stmt_holder import StmtHolder
from py_hcl.core.stmt_factory.trapper import StatementTrapper
from py_hcl.core.utils import module_inherit_mro
from . import merger
from . import extractor
from py_hcl.core.module.packed_module import PackedModule


def pack(bases, dct, name) -> PackedModule:
    raw_expr = extractor.extract(dct)
    raw_scope = StatementTrapper.trap()

    named_expr_list, statement_list = \
        handle_inherit(bases, raw_expr, raw_scope, name)

    res = PackedModule(name, named_expr_list, statement_list)
    return res


def handle_inherit(bases, named_expression, top_statement, name):
    modules = module_inherit_mro(bases)

    named_expr_list = \
        merger.merge_expr(modules, NamedExprHolder(name, named_expression))

    statement_list = \
        merger.merge_statement(modules, StmtHolder(name, top_statement))

    return named_expr_list, statement_list
