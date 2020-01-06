from py_hcl.core.expr import ExprTable


class Context(object):
    modules = {}
    expr_id_to_name = {}
    expr_obj_id_to_ref = {}
    expr_table = ExprTable.table
