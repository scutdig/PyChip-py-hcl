from py_hcl.core.expr_factory.add import do_add
from py_hcl.core.stmt_factory.connect import do_connect


class Expression(object):
    def __ilshift__(self, other):
        return do_connect(self, other)

    def __add__(self, other):
        return do_add(self, other)
