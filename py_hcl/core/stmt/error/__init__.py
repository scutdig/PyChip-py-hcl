from py_hcl.core.error import CoreError


def set_up():
    StatementError.append({
        'WrongBranchSyntax': {
            'code': 300,
            'value': StatementError(
                'expected a well-defined when-else_when-otherwise block')},
        'ConnectTypeError': {
            'code': 301,
            'value': StatementError(
                'connect statement contains unexpected types')
        }
    })


class StatementError(CoreError):
    @staticmethod
    def wrong_branch_syntax(msg):
        return StatementError.err('WrongBranchSyntax', msg)

    @staticmethod
    def connect_type_error(*args):
        ts = ', '.join([type(a.hcl_type).__name__ for a in args])
        msg = 'connect(): unsupported connect types: {}'.format(ts)
        return StatementError.err('ConnectTypeError', msg)


set_up()
