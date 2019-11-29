from .. import DslError


class ExprError(DslError):
    @staticmethod
    def io_value(msg):
        return ExprError.err('IOValueError', msg)


ExprError.append({
    'IOValueError': {
        'code': 200,
        'value': ExprError('io items should wrap with Input or Output')},
})
