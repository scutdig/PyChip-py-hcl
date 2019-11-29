from ...core import PyHclError


class ModuleErr(PyHclError):
    pass


err = {
    # Error Name    | Error value                  | Error Code
    'NotContainsIO': (ModuleErr('not contains io'), 0),
    'DuplicateName': (ModuleErr('duplicate names'), 1),
}


def module_err(name):
    return err[name][0]
