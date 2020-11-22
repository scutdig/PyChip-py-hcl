from py_hcl.core.expr.error import ExprError
from py_hcl.core.stmt.connect import VariableType


def ensure_all_args_are_values(f):
    """
    A helper decorator to ensure that the variable type of all arguments within
    a function call should be `VALUE` or `ASSIGNABLE_VALUE` if they are PyHCL
    expressions.

    It's useful to check validity when constructing nodes of binary operation
    like `add`, and unary operation like `invert`.

    Examples
    --------

    >>> from py_hcl import *
    >>> @ensure_all_args_are_values
    ... def f(*args):
    ...     pass


    Literals are `VALUE`s so they will pass the check:

    >>> f(U(10), S(30))


    Also for wires as they're `ASSIGNABLE_VALUE`s:

    >>> f(Wire(U.w(10)), Wire(S.w(10)))


    But not for output as they're `LOCATION`s:

    >>> class _(Module):
    ...     io = IO(o=Output(U.w(10)))
    ...     f(io.o)
    Traceback (most recent call last):
    ...
    py_hcl.core.expr.error.ExprError: Specified expresion has an invalid
    variable type
    """

    def _(*args):
        check_lists = [a for a in args if hasattr(a, 'variable_type')]
        sides = [VariableType.VALUE, VariableType.ASSIGNABLE_VALUE]

        for a in check_lists:
            if a.variable_type not in sides:
                msg = f'{a}\'s variable_type neither `VALUE` ' \
                      f'nor `ASSIGNABLE_VALUE`'
                raise ExprError.var_type_err(msg)

        return f(*args)

    return _
