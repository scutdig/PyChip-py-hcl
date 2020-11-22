from py_hcl.core.expr import ExprTable


class GlobalContext(object):
    modules = {}
    expr_id_to_name = {}
    expr_obj_id_to_ref = {}
    expr_table = ExprTable.table

    @staticmethod
    def clear():
        GlobalContext.modules.clear()
        GlobalContext.expr_id_to_name.clear()
        GlobalContext.expr_obj_id_to_ref.clear()
