from py_hcl.core.stmt_factory.trapper import StatementTrapper
from . import merger
from . import extractor
from py_hcl.core.module.packed_module import PackedModule


def pack(bases, dct, name):
    raw_expr = extractor.extract(dct, name)
    raw_scope = StatementTrapper.trap()

    named_expression, top_statement = \
        handle_inherit(bases, raw_expr, raw_scope, name)

    res = PackedModule(name, named_expression, top_statement)
    return res


def handle_inherit(bases, named_expression, top_statement, name):
    for b in bases:
        if not hasattr(b, 'packed_module'):
            continue

        pm = b.packed_module
        expr = pm.named_expressions
        ts = pm.top_statement

        named_expression = merger.merge_expr(named_expression, expr,
                                             (name, pm.name))
        top_statement = merger.merge_scope(top_statement, ts, (name, pm.name))

    return named_expression, top_statement
