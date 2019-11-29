from .merger import merge_expr, merge_scope
from .extractor import extract
from .packed_module import PackedModule


def pack(name, bases, dct):
    raw_expr = extract(dct)
    raw_scope = ...  # TODO

    named_expression, top_scope = handle_inherit(bases, raw_expr, raw_scope)

    res = PackedModule(name, named_expression, top_scope)
    return res


def handle_inherit(bases, named_expression, top_scope):
    for b in bases:
        if not hasattr(b, 'packed_module'):
            continue

        pm = b.packed_module
        expr = pm.named_expressions
        ts = pm.top_scope

        named_expression = merge_expr(named_expression, expr)
        top_scope = merge_scope(top_scope, ts)

    return named_expression, top_scope
