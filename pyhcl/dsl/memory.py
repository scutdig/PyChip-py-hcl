from __future__ import annotations
from dataclasses import dataclass, field, InitVar

from pyhcl.core._emit_context import EmitterContext
from pyhcl.core._repr import Node, CType, MemType
from pyhcl.ir import low_ir


@dataclass(eq=False)
class Mem(Node):
    size: int
    elemType: InitVar[CType]
    typ: MemType = field(init=False, default=None)

    def __post_init__(self, elemType):
        super().__post_init__()
        self.typ = MemType(self.size, elemType)

    def mapToIR(self, ctx: EmitterContext):
        name = ctx.getName(self)
        mtyp = self.typ.mapToIR(ctx)
        defm = low_ir.DefMemory(name, mtyp)
        ctx.appendFinalStatement(defm, self.scopeId)
        ref = low_ir.Reference(name, mtyp)
        ctx.updateRef(self, ref)
        return ref


