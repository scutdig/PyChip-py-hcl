from multipledispatch import dispatch

from ...stmt.block import Block

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Block)
def check(block: Block):
    from .. import check_all_stmt
    if not check_all_stmt(*block.statements):
        return False

    if len(block.statements) == 0:
        return False

    return True
