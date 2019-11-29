def set_up():
    ScopeManager.scope_list.append(
        {'scope_id': ScopeManager.next_id(), 'scope_type': ScopeType.GROUND}
    )


class ScopeType:
    GROUND = 0
    WHEN = 1
    ELSE_WHEN = 2
    OTHERWISE = 3


class ScopeManager(object):
    scope_list = []

    @classmethod
    def expand_scope(cls, scope_type):
        cls.scope_list.append(
            {'scope_id': cls.next_id(), 'scope_type': scope_type})

    @classmethod
    def shrink_scope(cls):
        cls.scope_list.pop()

    @classmethod
    def current_scope(cls):
        return cls.scope_list[-1]

    _next_scope_id = 0

    @classmethod
    def next_id(cls):
        ret = cls._next_scope_id
        cls._next_scope_id += 1
        return ret


class Scope(object):
    def __init__(self, stmts):
        self.statements = stmts


set_up()
