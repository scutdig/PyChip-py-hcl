from py_hcl.core.error import CoreError


def set_up():
    StatementError.append({
        'WrongBranchSyntax': {
            'code': 300,
            'value': StatementError(
                'expected a well-defined when-else_when-otherwise block')},

    })


class StatementError(CoreError):
    @staticmethod
    def wrong_branch_syntax(msg):
        return StatementError.err('WrongBranchSyntax', msg)


set_up()
