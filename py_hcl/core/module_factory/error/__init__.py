from py_hcl.core.error import CoreError


def set_up():
    ModuleError.append({
        'NotContainsIO': {
            'code': 100,
            'value': ModuleError('the module lack of io attribute')},
    })


class ModuleError(CoreError):
    @staticmethod
    def not_contains_io(msg):
        return ModuleError.err('NotContainsIO', msg)


set_up()
