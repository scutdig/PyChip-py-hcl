from dataclasses import dataclass, field
from typing import Union, Generator, List

from pyhcl.core._repr import CType, Node
from pyhcl.core._emit_context import EmitterContext
from pyhcl.core._utils import get_attr
from pyhcl.ir import low_ir


@dataclass
class Vec(CType):
    size: int
    typ: CType
    lvl: int = field(init=False, default=1)

    def __post_init__(self):
        if self.size <= 0:
            raise Exception("can not declare an empty vector")

        if get_attr(self.typ, "lvl") is not None:
            self.lvl = self.typ.lvl + 1
        else:
            self.lvl = 1

    def mapToIR(self, ctx: EmitterContext):
        typ = self.typ.mapToIR(ctx)
        return low_ir.VectorType(typ, self.size)


@dataclass(init=False)
class VecInit(Node):
    lst: List[Node]
    typ: CType = field(init=False, default=None)
    lvl: int = field(init=False, default=1)

    def __init__(self, lst: Union[Generator, list]):
        super().__post_init__()
        lst = list(lst)

        if len(lst) <= 0:
            raise Exception("can not declare an empty vector")

        self.lst = lst
        self.typ = Vec(len(self.lst), self.lst[0].typ)
        lvl = get_attr(self.lst[0], "lvl")
        self.lvl = 1 + (lvl if lvl is not None else 0)
        self.typ.lvl = self.lvl

    def __iter__(self):
        return iter(self.lst)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.lst[item]
        else:
            return super().__getitem__(item)

    def __len__(self):
        return len(self.lst)

    def size(self):
        return len(self)

    def length(self):
        return len(self)

    def flatten(self):
        if isinstance(self.lst[0], VecInit):
            return VecInit([j for i in self.lst for j in i])
        else:
            raise Exception("Vector with initiate values can not be flatten with raw vector")

    def reverse(self):
        return VecInit(list(reversed(self.lst[:])))

    def mapToIR(self, ctx: EmitterContext):
        # Define Wire
        name = ctx.getName(self)
        typ = self.typ.mapToIR(ctx)
        wire = low_ir.DefWire(name, typ)
        ctx.appendFinalStatement(wire, self.scopeId)
        ref = low_ir.Reference(name, typ)
        ctx.updateRef(self, ref)

        # Connect Elements
        for i, node in enumerate(self.lst):
            for idx, elem in self.subIdxs(low_ir.SubIndex(ref, i, typ.typ), node, ctx):
                con = low_ir.Connect(idx, elem)
                ctx.appendFinalStatement(con, self.scopeId)

        return ref

    def subIdxs(self, idx, node, ctx):
        if isinstance(node, VecInit):
            return [(nIdx, elem) for i, n in enumerate(node.lst)
                    for nIdx, elem in node.subIdxs(low_ir.SubIndex(idx, i, node.typ.mapToIR(ctx)), n, ctx)]
        else:
            return [(idx, node.mapToIR(ctx))]
