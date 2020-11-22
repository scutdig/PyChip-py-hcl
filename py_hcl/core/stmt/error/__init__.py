from py_hcl.core.error import CoreError


def set_up():
    StatementError.append({
        'WrongBranchSyntax': {
            'code':
            300,
            'value':
            StatementError(
                'expected a well-defined when-else_when-otherwise block')
        },
        'ConnectTypeError': {
            'code': 301,
            'value':
            StatementError('Connect statement contains unexpected type.')
        },
        'ConnectDirectionError': {
            'code':
            302,
            'value':
            StatementError('Connection statement with unexpected direction.')
        }
    })


class StatementError(CoreError):
    @staticmethod
    def wrong_branch_syntax(msg):
        return StatementError.err('WrongBranchSyntax', msg)

    @staticmethod
    def connect_type_error(*args):
        ts = ', '.join([type(a.hcl_type).__name__ for a in args])
        msg = 'connect(): unsupported connect type: {}'.format(ts)
        return StatementError.err('ConnectTypeError', msg)

    @staticmethod
    def connect_direction_error(msg):
        return StatementError.err('ConnectDirectionError', msg)


set_up()
