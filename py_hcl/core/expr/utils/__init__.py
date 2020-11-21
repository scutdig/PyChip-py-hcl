from py_hcl.core.stmt.connect import VariableType


def ensure_all_args_are_values(f):
    def _(*args):
        check_lists = [a for a in args if hasattr(a, 'variable_type')]
        sides = [VariableType.VALUE, VariableType.ASSIGNABLE_VALUE]

        # TODO: Accurate Error Message
        assert all(a.variable_type in sides for a in check_lists)
        return f(*args)

    return _
