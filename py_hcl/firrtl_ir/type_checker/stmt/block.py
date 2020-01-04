from multipledispatch import dispatch
import logging

from ...stmt.block import Block

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Block)
def check(block: Block):
    from .. import check_all_stmt
    if not check_all_stmt(*block.statements):
        logging.error("block: statements check failed")
        return False

    if len(block.statements) == 0:
        logging.error("block: number of statements is 0")
        return False

    return True
