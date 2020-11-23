from py_hcl.transformer.pyhcl_to_firrtl.global_context import GlobalContext
from py_hcl.utils import get_key_by_value


def build_io_name(module_name: str, field_name: str):
    return module_name + "_io_" + field_name


def build_reserve_name(module_name: str, expr_name: str):
    return "_" + module_name + "_" + expr_name


def get_io_obj(packed_module):
    table = packed_module.named_expr_chain[0].named_expression_table
    io_id = get_key_by_value(table, 'io')
    return GlobalContext.expr_table[io_id]
