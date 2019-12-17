from py_hcl.core.module_factory.error import ModuleError
from py_hcl.core.expr import HclExpr


def extract(dct, name):
    res = {}

    for k, v in dct.items():
        # TODO: check if is source not composed expression
        if isinstance(v, HclExpr):
            res[k] = v

    check_io_exist(res, name)

    return res


def check_io_exist(res, name):
    if 'io' not in res:
        raise ModuleError.not_contains_io(
            'module {} lack of io attribute'.format(name))
