from py_hcl.core.error import CoreError


def set_up():
    ExprError.append({
        'IOValueError': {
            'code': 200,
            'value':
            ExprError('IO items should be wrapped with Input or Output.')
        },
        'OpTypeError': {
            'code': 201,
            'value': ExprError('Specified arguments contain unexpected type.')
        },
        'OutOfRangeError': {
            'code': 202,
            'value':
            ExprError('Specified value out of range for the given type')
        }
    })


class ExprError(CoreError):
    @staticmethod
    def io_value_err(msg):
        return ExprError.err('IOValueError', msg)

    @staticmethod
    def op_type_err(op, *args):
        ts = ', '.join([type(a.hcl_type).__name__ for a in args])
        msg = '{}(): unsupported operand type: {}'.format(op, ts)
        return ExprError.err('OpTypeError', msg)

    @staticmethod
    def out_of_range(msg):
        return ExprError.err('OutOfRangeError', msg)


set_up()
