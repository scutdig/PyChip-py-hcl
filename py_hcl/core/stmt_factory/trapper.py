from .scope import Scope, ScopeManager, ScopeType


class StatementTrapper(object):
    trapped_stmts = []

    @classmethod
    def trap(cls):
        ScopeManager.shrink_scope()

        ret = Scope(cls.trapped_stmts)
        cls.trapped_stmts = []

        ScopeManager.expand_scope(ScopeType.GROUND)
        return ret  # TODO

    @classmethod
    def trace(cls, statement):
        # TODO: wrap the statement
        print("StatementTrapper.trace: need wrap the statement")

        statement = {
            'scope': ScopeManager.current_scope(),
            'statement': statement,
        }

        cls.trapped_stmts.append(statement)
