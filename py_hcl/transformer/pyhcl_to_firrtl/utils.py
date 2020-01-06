from py_hcl.transformer.pyhcl_to_firrtl.context import Context


def build_io_name(module_name: str, field_name: str):
    return module_name + "_io_" + field_name


def build_reserve_name(module_name: str, expr_name: str):
    return "_" + module_name + "_" + expr_name


def get_io_obj(packed_module):
    table = packed_module.named_expr_chain.named_expr_chain_head \
        .named_expr_holder.named_expression_table
    io_id = list(table.keys())[list(table.values()).index('io')]
    return Context.expr_table[io_id]
