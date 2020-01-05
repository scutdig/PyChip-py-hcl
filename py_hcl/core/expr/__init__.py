from multipledispatch.dispatcher import MethodDispatcher

from py_hcl.core.hcl_ops import op_apply
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type import UnknownType, HclType
from py_hcl.utils import json_serialize


class ExprIdGen:
    id = -1

    @classmethod
    def next_id(cls):
        cls.id += 1
        return cls.id


class ExprTable:
    table = {}

    @classmethod
    def add(cls, i, obj):
        cls.table[i] = obj

    @classmethod
    def get(cls, i):
        return cls.table[i]


@json_serialize
class HclExpr(object):
    hcl_type = UnknownType()
    conn_side = ConnSide.UNKNOWN

    def __new__(cls, *args):
        obj = super().__new__(cls)
        obj.id = ExprIdGen.next_id()
        ExprTable.add(obj.id, obj)
        return obj

    def __ilshift__(self, other):
        return op_apply('<<=')(self, other)

    def __add__(self, other):
        return op_apply('+')(self, other)

    def __and__(self, other):
        return op_apply('&')(self, other)

    def __or__(self, other):
        return op_apply('|')(self, other)

    def __xor__(self, other):
        return op_apply('^')(self, other)

    def __getattr__(self, item):
        return op_apply('.')(self, item)

    def __setitem__(self, key, value):
        return self[key]

    __getitem__ = MethodDispatcher('__getitem__')

    @__getitem__.register(tuple)
    def _(self, item):
        if len(item) == 1:
            return self[item[0]]
        return self.__getitem__(item[0])[item[1:]]

    @__getitem__.register(slice)
    def _(self, item):
        start = item.start if item.start is not None else 0
        if item.step is None:
            if item.stop is not None:
                return op_apply('[i:j]')(self, start, item.stop)
            if item.stop is None:
                return op_apply('[i:]')(self, start)
        if item.stop is not None:
            return op_apply('[i:j:k]')(self, start, item.stop, item.step)
        if item.stop is None:
            return op_apply('[i::k]')(self, start, item.step)

    @__getitem__.register(int)
    def _(self, item):
        return op_apply('[i]')(self, item)

    def to_uint(self):
        return op_apply('to_uint')(self)

    def to_sint(self):
        return op_apply('to_sint')(self)

    def to_bool(self):
        return op_apply('to_bool')(self)


@json_serialize(json_fields=['id', 'type', 'hcl_type', 'conn_side', 'op_node'])
class ExprHolder(HclExpr):
    def __init__(self, hcl_type: HclType, conn_side: ConnSide, op_node):
        self.type = 'expr_holder'
        self.hcl_type = hcl_type
        self.conn_side = conn_side
        self.op_node = op_node
