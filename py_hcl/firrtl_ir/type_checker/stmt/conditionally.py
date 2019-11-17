from py_hcl.firrtl_ir.shortcuts import uw
from py_hcl.firrtl_ir.stmt.conditionally import Conditionally
from ...type_measurer import equal


class ConditionallyTypeChecker(object):
    conditionally_checker_map = {}

    @staticmethod
    def check(op_obj):
        try:
            return ConditionallyTypeChecker \
                .conditionally_checker_map[type(op_obj)](op_obj)
        except KeyError:
            raise NotImplementedError(type(op_obj))


def checker(connect):
    def f(func):
        ConditionallyTypeChecker.conditionally_checker_map[connect] = func
        return func

    return f


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Conditionally)
def _(cond):
    from .. import check_all_expr, check_all_stmt
    if not check_all_expr(cond.pred_ref):
        return False

    if not check_all_stmt(cond.seq, cond.alt):
        return False

    if not equal(cond.pred_ref.tpe, uw(1)):
        return False

    return True
