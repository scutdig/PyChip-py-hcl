from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.error import StatementError
from py_hcl.core.stmt_factory.scope import ScopeManager, ScopeType
from py_hcl.core.stmt_factory.trapper import StatementTrapper
from py_hcl.core.type.uint import UIntT
from py_hcl.utils import auto_repr


@auto_repr
class When(object):
    def __init__(self, cond: HclExpr):
        self.cond = cond


@auto_repr
class ElseWhen(object):
    def __init__(self, cond: HclExpr):
        self.cond = cond


@auto_repr
class Otherwise(object):
    pass


def do_when_enter(cond_expr: HclExpr):
    check_bool_expr(cond_expr)

    w = When(cond_expr)
    ScopeManager.expand_scope(ScopeType.WHEN, w)


def do_when_exit():
    ScopeManager.shrink_scope()


def do_else_when_enter(cond_expr: HclExpr):
    check_bool_expr(cond_expr)
    check_branch_syntax()

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


def check_bool_expr(cond_expr: HclExpr):
    if isinstance(cond_expr.hcl_type, UIntT) and cond_expr.hcl_type.width == 1:
        return
    raise StatementError.wrong_branch_syntax(
        'check_bool_expr(): '
        'expected bool-type expression')


def check_branch_syntax():
    check_exists_pre_stmts()
    check_exists_pre_when_block()
    check_correct_block_level()


def check_exists_pre_stmts():
    if len(StatementTrapper.trapped_stmts[-1]) == 0:
        raise StatementError.wrong_branch_syntax(
            'check_exists_pre_stmts(): '
            'expected when block')


def check_exists_pre_when_block():
    last_stmt = StatementTrapper.trapped_stmts[-1][-1]
    last_scope = last_stmt['scope']
    last_scope_type = last_scope['scope_type']

    not_when = last_scope_type != ScopeType.WHEN
    not_else_when = last_scope_type != ScopeType.ELSE_WHEN
    if not_when and not_else_when:
        raise StatementError.wrong_branch_syntax(
            'check_exists_pre_when_block(): '
            'expected when block or else_when block')


def check_correct_block_level():
    last_stmt = StatementTrapper.trapped_stmts[-1][-1]
    last_scope = last_stmt['scope']
    current_scope = ScopeManager.current_scope()
    last_scope_level = last_scope['scope_level']
    current_scope_level = current_scope['scope_level']
    if last_scope_level != current_scope_level + 1:
        raise StatementError.wrong_branch_syntax(
            'check_correct_block_level(): '
            'branch block not matched')
