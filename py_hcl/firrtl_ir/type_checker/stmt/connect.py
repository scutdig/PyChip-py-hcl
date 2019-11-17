from ...type_measurer import equal
from ...stmt.connect import Connect


class ConnectTypeChecker(object):
    connect_checker_map = {}

    @staticmethod
    def check(op_obj):
        try:
            return ConnectTypeChecker.connect_checker_map[type(op_obj)](op_obj)
        except KeyError:
            raise NotImplementedError(type(op_obj))


def checker(connect):
    def f(func):
        ConnectTypeChecker.connect_checker_map[connect] = func
        return func

    return f


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Connect)
def _(connect):
    from .. import check_all_expr
    if not check_all_expr(connect.loc_ref, connect.expr_ref):
        return False

    if not equal(connect.loc_ref.tpe, connect.expr_ref.tpe):
        return False

    return True
