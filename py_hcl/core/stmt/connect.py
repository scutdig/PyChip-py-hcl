from py_hcl.core.expr import ConnDir
from py_hcl.core.hcl_ops import hcl_operation
from py_hcl.core.stmt.trapper import StatementTrapper


class Connect(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


connector = hcl_operation('<<=')


@connector(object, object)
def _(left, right):
    check_connect_dir(left, right)
    # TODO: need some check
    print('do_connect: need some check')

    StatementTrapper.track(Connect(left, right))

    return left


def check_connect_dir(left, right):
    assert left.conn_dir in (ConnDir.LF, ConnDir.BOTH)
    assert right.conn_dir in (ConnDir.RT, ConnDir.BOTH)
