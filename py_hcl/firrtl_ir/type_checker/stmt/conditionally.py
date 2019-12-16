from multipledispatch import dispatch

from ...shortcuts import uw
from ...stmt.conditionally import Conditionally
from ...type_measurer import equal

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Conditionally)
def check(cond: Conditionally):
    from .. import check_all_expr, check_all_stmt
    if not check_all_expr(cond.pred_ref):
        return False

    if not check_all_stmt(cond.seq, cond.alt):
        return False

    if not equal(cond.pred_ref.tpe, uw(1)):
        return False

    return True
