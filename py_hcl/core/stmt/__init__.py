from py_hcl.utils import auto_repr


@auto_repr
class LineStatement(object):
    def __init__(self, scope_id, statement):
        self.scope_id = scope_id
        self.statement = statement


@auto_repr
class BlockStatement(object):
    def __init__(self, scope_info, stmts):
        self.scope_info = scope_info
        self.statements = stmts
