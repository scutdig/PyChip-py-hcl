from ...stmt.block import Block


class BlockTypeChecker(object):
    block_checker_map = {}

    @staticmethod
    def check(op_obj):
        try:
            return BlockTypeChecker.block_checker_map[type(op_obj)](op_obj)
        except KeyError:
            raise NotImplementedError(type(op_obj))


def checker(connect):
    def f(func):
        BlockTypeChecker.block_checker_map[connect] = func
        return func

    return f


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(Block)
def _(block):
    from .. import check_all_stmt
    if not check_all_stmt(*block.statements):
        return False

    return True
