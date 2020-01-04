import logging

from multipledispatch import dispatch

from ...stmt.connect import Connect
from ...type_measurer import equal

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Connect)
def check(connect: Connect):
    from .. import check_all_expr
    if not check_all_expr(connect.loc_ref, connect.expr_ref):
        logging.error("connect: lhs or rhs reference check failed")
        return False

    if not equal(connect.loc_ref.tpe, connect.expr_ref.tpe):
        logging.error("connect: type unmatched - {} & {}".format(
            connect.loc_ref.tpe, connect.expr_ref.tpe
        ))
        return False

    return True
