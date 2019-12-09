from py_hcl.core.stmt_factory.trapper import StatementTrapper


class Connect(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


def do_connect(left, right):
    # TODO: need some check
    print('do_connect: need some check')

    StatementTrapper.track(Connect(left, right))

    return left
