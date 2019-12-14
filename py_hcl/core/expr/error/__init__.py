from py_hcl.core.error import CoreError


def set_up():
    ExprError.append({
        'IOValueError': {
            'code': 200,
            'value': ExprError('io items should wrap with Input or Output')},
        'AddError': {
            'code': 201,
            'value': ExprError('specified arguments contain unexpected types')
        }
    })


class ExprError(CoreError):
    @staticmethod
    def io_value(msg):
        return ExprError.err('IOValueError', msg)

    @staticmethod
    def add(lf, rt):
        return ExprError.err('AddError',
                             'unsupported operand types: {} and {}'.format(
                                 type(lf), type(rt)))


set_up()
