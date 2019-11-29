class PackedModule(object):
    def __init__(self, name, named_expressions, top_scope):
        self.name = name
        self.named_expressions = named_expressions
        self.top_scope = top_scope
