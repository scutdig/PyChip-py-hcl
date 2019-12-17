from py_hcl.core.error import CoreError


def set_up():
    ExprError.append({
        'IOValueError': {
            'code': 200,
            'value': ExprError('io items should wrap with Input or Output')},
        'OpTypeError': {
            'code': 201,
            'value': ExprError('specified arguments contain unexpected types')
        }
    })


class ExprError(CoreError):
    @staticmethod
    def io_value(msg):
        return ExprError.err('IOValueError', msg)

    @staticmethod
    def op_type_err(op, *args):
        ts = ', '.join([type(a.hcl_type).__name__ for a in args])
        msg = '{}(): unsupported operand types: {}'.format(op, ts)
        return ExprError.err('OpTypeError', msg)


set_up()
