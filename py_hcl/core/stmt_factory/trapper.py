from .scope import Scope, ScopeManager, ScopeType


def set_up():
    ScopeManager.register_scope_expanding(
        StatementTrapper.when_scope_expanding)
    ScopeManager.register_scope_shrinking(
        StatementTrapper.when_scope_shrinking
    )
    ScopeManager.expand_scope(ScopeType.GROUND)


class StatementTrapper(object):
    trapped_stmts = [[
        # TOP SCOPE which contains all modules
    ]]

    @classmethod
    def trap(cls):
        ScopeManager.shrink_scope()

        assert len(cls.trapped_stmts) == 1
        t = cls.trapped_stmts[0][-1]
        ret = Scope(t['scope'], t['statement'])

        ScopeManager.expand_scope(ScopeType.GROUND)

        return ret  # TODO

    @classmethod
    def track(cls, statement):
        # TODO: wrap the statement
        print("StatementTrapper.trace: need wrap the statement")

        statement = {
            'scope': ScopeManager.current_scope(),
            'statement': statement,
        }
        cls.trapped_stmts[-1].append(statement)

    @classmethod
    def when_scope_expanding(cls, current_scope, next_scope):
        cls.trapped_stmts.append([])

    @classmethod
    def when_scope_shrinking(cls, current_scope, next_scope):
        stmts = cls.trapped_stmts.pop()
        cls.trapped_stmts[-1].append({
            'scope': current_scope,
            'statement': stmts
        })


set_up()
