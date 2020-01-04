import logging

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
        logging.error("conditionally: cond reference check failed")
        return False

    if not check_all_stmt(cond.seq, cond.alt):
        logging.error("conditionally: seq or alt statements check failed")
        return False

    if not equal(cond.pred_ref.tpe, uw(1)):
        logging.error("conditionally: cond reference type check failed")
        return False

    return True
