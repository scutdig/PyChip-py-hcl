from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from pyhcl.core._emit_context import EmitterContext
from pyhcl.core._repr import Declare, Node
from pyhcl.ir import low_ir


@dataclass
class CondBlock(Declare):
    when: When = None
    elsewhens: List[Elsewhen] = field(init=False, default_factory=list)
    otherwise: Otherwise = field(init=False, default=None)

    __canAcceptOtherwise: bool = field(init=False, default=True, repr=False)
    __canAcceptElsewhen: bool = field(init=False, default=True, repr=False)

    def withElsewhen(self, elifBlock):
        self.elsewhens.append(elifBlock)
        return self

    def withOtherwise(self, elseBlock):
        self.__canAcceptOtherwise = False
        self.__canAcceptElsewhen = False
        self.otherwise = elseBlock
        return self

    def canAcceptElsewhen(self):
        return self.__canAcceptElsewhen

    def canAcceptOtherwise(self):
        return self.__canAcceptOtherwise

    def mapToIR(self, ctx: EmitterContext):
        def _mapToIRRec(cb: CondBlock):
            cond = ctx.getRef(cb.when.cond)
            [ctx.getRef(i) for i in cb.when.block]
            conseq = low_ir.Block(ctx.getScopeStatements(cb.when.ownScope))
            if len(cb.elsewhens) == 0:
                if cb.otherwise is None:
                    alt = low_ir.EmptyStmt()
                else:
                    [ctx.getRef(i) for i in cb.otherwise.block]
                    alt = low_ir.Block(ctx.getScopeStatements(cb.otherwise.ownScope))
                return low_ir.Conditionally(cond, conseq, alt)
            else:
                elif_ = cb.elsewhens[0]
                a = When(elif_.cond, elif_.block)
                a.ownScope = elif_.ownScope
                ncb = CondBlock(a)
                for i in cb.elsewhens[1:]:
                    ncb.withElsewhen(i)
                ncb.withOtherwise(cb.otherwise)
                alt = _mapToIRRec(ncb)
                return low_ir.Conditionally(cond, conseq, alt)

        stmt = _mapToIRRec(self)
        ctx.appendFinalStatement(stmt, self.scopeId)
        return stmt


@dataclass
class When:
    cond: Node
    block: List[Node]
    ownScope: int = field(init=False, repr=False, default=None)


@dataclass
class Elsewhen:
    cond: Node
    block: List[Node]
    ownScope: int = field(init=False, repr=False, default=None)


@dataclass
class Otherwise:
    block: List[Node]
    ownScope: int = field(init=False, repr=False, default=None)