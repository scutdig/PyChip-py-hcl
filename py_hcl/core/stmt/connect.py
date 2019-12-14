from py_hcl.core.hcl_ops import hcl_operation
from py_hcl.core.stmt.trapper import StatementTrapper


class Connect(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


@hcl_operation('<<=')
def do_connect(left, right):
    # TODO: need some check
    print('do_connect: need some check')

    StatementTrapper.track(Connect(left, right))

    return left
