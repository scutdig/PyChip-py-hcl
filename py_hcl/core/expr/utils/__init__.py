from py_hcl.core.stmt.connect import VariableType


def assert_right_side(f):
    def _(*args):
        check_lists = [a for a in args if hasattr(a, 'variable_type')]
        sides = [VariableType.VALUE, VariableType.ASSIGNABLE_VALUE]

        # TODO: Accurate Error Message
        assert all(a.variable_type in sides for a in check_lists)
        return f(*args)

    return _
