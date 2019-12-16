from enum import Enum

from py_hcl.core.hcl_ops import hcl_call
from py_hcl.core.type import HclType
from py_hcl.utils import auto_repr


class ConnDir(Enum):
    UNKNOWN = 0
    LF = 1
    RT = 2
    BOTH = 3


@auto_repr
class HclExpr(object):
    def __init__(self):
        self.hcl_type = HclType()
        self.conn_dir = ConnDir.UNKNOWN

    def __ilshift__(self, other):
        return hcl_call('<<=')(self, other)

    def __add__(self, other):
        return hcl_call('+')(self, other)

    def __getattr__(self, item):
        return hcl_call('.')(self, item)
