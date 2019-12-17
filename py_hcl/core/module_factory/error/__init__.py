from py_hcl.core.error import CoreError


def set_up():
    ModuleError.append({
        'NotContainsIO': {
            'code': 100,
            'value': ModuleError('the module lack of io attribute')},

        'InheritDuplicateName': {
            'code': 101,
            'value': ModuleError('modules with inherited relationships '
                                 'contain duplicate attributes')},
    })


class ModuleError(CoreError):
    @staticmethod
    def not_contains_io(msg):
        return ModuleError.err('NotContainsIO', msg)

    @staticmethod
    def duplicate_name(msg):
        return ModuleError.err('InheritDuplicateName', msg)


set_up()
