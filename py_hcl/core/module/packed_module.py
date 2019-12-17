from py_hcl.utils import auto_repr


@auto_repr
class PackedModule(object):
    def __init__(self, name, named_expressions, top_statement):
        self.name = name
        self.named_expressions = named_expressions
        self.top_statement = top_statement
