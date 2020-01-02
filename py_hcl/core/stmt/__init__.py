from py_hcl.utils import json_serialize


@json_serialize
class LineStatement(object):
    def __init__(self, scope_id, statement):
        self.stmt_class = 'line'
        self.scope_id = scope_id
        self.statement = statement


@json_serialize
class ClusterStatement(object):
    def __init__(self, scope_info, stmts):
        self.stmt_class = 'cluster'
        self.scope_info = scope_info
        self.statements = stmts
