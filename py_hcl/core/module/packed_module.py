from py_hcl.utils import json_serialize


@json_serialize
class PackedModule(object):
    def __init__(self, name, named_expr_chain, statement_chain):
        self.name = name
        self.named_expr_chain = named_expr_chain
        self.statement_chain = statement_chain
