from multipledispatch import dispatch

from ...expr.mux import Mux
from ...shortcuts import uw
from ...type_measurer import equal

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Mux)
def check(mux: Mux):
    from .. import check_all_expr
    if not check_all_expr(mux.cond, mux.tval, mux.fval):
        return False
    if not equal(mux.cond.tpe, uw(1)):
        return False
    if not equal(mux.tval.tpe, mux.fval.tpe):
        return False
    if not equal(mux.tval.tpe, mux.tpe):
        return False
    return True
