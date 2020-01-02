from py_hcl.core.stmt import LineStatement, ClusterStatement
from .scope import ScopeManager, ScopeType


def set_up():
    ScopeManager.register_scope_expanding(
        StatementTrapper.on_scope_expanding)
    ScopeManager.register_scope_shrinking(
        StatementTrapper.on_scope_shrinking)
    ScopeManager.expand_scope(ScopeType.GROUND)


class StatementTrapper(object):
    trapped_stmts = [[
        # TOP SCOPE which contains all modules
    ]]

    @classmethod
    def trap(cls):
        ScopeManager.shrink_scope()

        assert len(cls.trapped_stmts) == 1
        ret = cls.trapped_stmts[0][-1]

        ScopeManager.expand_scope(ScopeType.GROUND)

        return ret  # TODO

    @classmethod
    def track(cls, statement):
        statement = LineStatement(
            ScopeManager.current_scope().scope_id,
            statement
        )
        cls.trapped_stmts[-1].append(statement)

    @classmethod
    def on_scope_expanding(cls, current_scope, next_scope):
        cls.trapped_stmts.append([])

    @classmethod
    def on_scope_shrinking(cls, current_scope, next_scope):
        stmts = cls.trapped_stmts.pop()
        cls.trapped_stmts[-1].append(ClusterStatement(current_scope, stmts))


set_up()
