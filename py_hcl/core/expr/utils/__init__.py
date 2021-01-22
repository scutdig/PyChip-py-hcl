from py_hcl.core.expr.error import ExprError
from py_hcl.core.stmt.connect import VariableType


def ensure_all_args_are_readable(f):
    """
    A helper decorator to ensure that the variable type of all arguments within
    a function call should be `ReadOnly` or `ReadWrite` if they are PyHCL
    expressions.

    It's useful to check validity when constructing nodes of binary operation
    like `add`, and unary operation like `invert`.

    Examples
    --------

    >>> from py_hcl import *
    >>> @ensure_all_args_are_readable
    ... def f(*args):
    ...     pass


    Literals are `ReadOnly` so they will pass the check:

    >>> f(U(10), S(30))


    Also for wires as they're `ReadWrite`:

    >>> f(Wire(U.w(10)), Wire(S.w(10)))


    But not for output as they're `WriteOnly`:

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
        sides = [VariableType.ReadOnly, VariableType.ReadWrite]

        for a in check_lists:
            if a.variable_type not in sides:
                msg = f'{a}\'s variable_type neither `ReadOnly` ' \
                      f'nor `ReadWrite`'
                raise ExprError.var_type_err(msg)

        return f(*args)

    return _
