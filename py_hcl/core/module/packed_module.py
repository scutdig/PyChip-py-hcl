from py_hcl.utils import auto_repr


@auto_repr
class PackedModule(object):
    def __init__(self, name, named_expr_list, statement_list):
        self.name = name
        self.named_expr_list = named_expr_list
        self.statement_list = statement_list
