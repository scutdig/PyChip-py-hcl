from py_hcl.utils import json_serialize


@json_serialize(json_fields=['stmt_class', 'statement'])
class LineStatement(object):
    def __init__(self, scope_id, statement):
        self.stmt_class = 'line'
        self.scope_id = scope_id
        self.statement = statement


@json_serialize(json_fields=['stmt_class', 'statements'])
class ClusterStatement(object):
    def __init__(self, scope_info, stmts):
        self.stmt_class = 'cluster'
        self.scope_info = scope_info
        self.statements = stmts


@json_serialize
class ConditionStatement(object):
    def __init__(self, seq_cond_id, seq_stmts, alt_stmts):
        self.stmt_class = 'condition'
        self.seq_cond_id = seq_cond_id
        self.seq_stmts = seq_stmts
        self.alt_stmts = alt_stmts
