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
        },
        'VarTypeError': {
            'code': 203,
            'value':
            ExprError('Specified expresion has an invalid variable type')
        },
        'UnmatchedVecSizeError': {
            'code': 204,
            'value': ExprError('Sizes of vectors are unmatched')
        }
    })


class ExprError(CoreError):
    @staticmethod
    def io_value_err(msg: str):
        return ExprError.err('IOValueError', msg)

    @staticmethod
    def op_type_err(op, *args):
        ts = ', '.join([type(a.hcl_type).__name__ for a in args])
        msg = '{}(): unsupported operand type: {}'.format(op, ts)
        return ExprError.err('OpTypeError', msg)

    @staticmethod
    def out_of_range_err(msg: str):
        return ExprError.err('OutOfRangeError', msg)

    @staticmethod
    def var_type_err(msg: str):
        return ExprError.err('VarTypeError', msg)

    @staticmethod
    def unmatched_vec_size(size0: int, size1: int):
        return ExprError.err('UnmatchedVecSizeError', f'{size0} != {size1}')


set_up()
