from py_hcl.core.stmt_factory import StatementError
from py_hcl.core.stmt_factory.scope import ScopeManager, ScopeType
from py_hcl.core.stmt_factory.trapper import StatementTrapper


class When(object):
    def __init__(self, cond):
        self.cond = cond


class ElseWhen(object):
    def __init__(self, cond):
        self.cond = cond


class Otherwise(object):
    pass


def do_when_enter(cond_expr):
    # TODO: need some checks
    print('do_when_enter: need some check')

    w = When(cond_expr)
    ScopeManager.expand_scope(ScopeType.WHEN, w)


def do_when_exit():
    ScopeManager.shrink_scope()


def do_else_when_enter(cond_expr):
    check_branch_syntax()

    # TODO: need some checks
    print('do_else_when_enter: need some check')

    e = ElseWhen(cond_expr)
    ScopeManager.expand_scope(ScopeType.ELSE_WHEN, e)


def do_else_when_exit():
    ScopeManager.shrink_scope()


def do_otherwise_enter():
    check_branch_syntax()

    o = Otherwise()
    ScopeManager.expand_scope(ScopeType.OTHERWISE, o)


def do_otherwise_exit():
    ScopeManager.shrink_scope()


def check_branch_syntax():
    if len(StatementTrapper.trapped_stmts[-1]) == 0:
        raise StatementError.wrong_branch_syntax('expected when block')

    last_stmt = StatementTrapper.trapped_stmts[-1][-1]
    last_scope = last_stmt['scope']
    last_scope_type = last_scope['scope_type']
    if last_scope_type != ScopeType.WHEN and \
            last_scope_type != ScopeType.ELSE_WHEN:
        raise StatementError.wrong_branch_syntax('expected when block or '
                                                 'else_when block')

    current_scope = ScopeManager.current_scope()
    last_scope_level = last_scope['scope_level']
    current_scope_level = current_scope['scope_level']
    if last_scope_level != current_scope_level + 1:
        raise StatementError.wrong_branch_syntax('branch block not matched')
