from enum import Enum
import logging

from multipledispatch.dispatcher import MethodDispatcher

from py_hcl.core.hcl_ops import op_apply
from py_hcl.core.type import UnknownType, HclType
from py_hcl.utils import auto_repr


class ConnDir(Enum):
    UNKNOWN = 0
    LF = 1
    RT = 2
    BOTH = 3


@auto_repr
class HclExpr(object):
    hcl_type = UnknownType()
    conn_dir = ConnDir.UNKNOWN

    def __ilshift__(self, other):
        return op_apply('<<=')(self, other)

    def __add__(self, other):
        return op_apply('+')(self, other)

    def __getattr__(self, item):
        return op_apply('.')(self, item)

    __getitem__ = MethodDispatcher('__getitem__')

    @__getitem__.register(tuple)
    def _(self, item):
        logging.warning('slice(): too many index blocks, '
                        'only the first one takes effect')
        item = item[0]
        return self.__getitem__(item)

    @__getitem__.register(slice)
    def _(self, item):
        """
        o[5:2]
        """
        assert item.start is not None
        assert item.stop is not None
        assert item.step is None
        return op_apply('[i:j]')(self, item.start, item.stop)

    @__getitem__.register(int)
    def _(self, item):
        """
        o[5]
        """
        return op_apply('[i]')(self, item)

    def to_uint(self):
        return op_apply('to_uint')(self)

    def to_sint(self):
        return op_apply('to_sint')(self)

    def to_bool(self):
        return op_apply('to_bool')(self)


class ExprHolder(HclExpr):
    def __init__(self, hcl_type: HclType, conn_dir: ConnDir, assoc_value):
        self.hcl_type = hcl_type
        self.conn_dir = conn_dir
        self.assoc_value = assoc_value
