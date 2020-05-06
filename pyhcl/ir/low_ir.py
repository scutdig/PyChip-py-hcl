from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional

from pyhcl.ir.low_node import FirrtlNode
from pyhcl.ir.low_prim import PrimOp, Bits
from pyhcl.ir.utils import indent


class Info(FirrtlNode, ABC):
    """INFOs"""

    def serialize(self) -> str:
        """default implementation"""
        return self.__repr__()


@dataclass(frozen=True, init=False)
class NoInfo(Info):
    def serialize(self) -> str:
        return ''


@dataclass(frozen=True)
class FileInfo(Info):
    info: StringLit

    def serialize(self) -> str:
        return f" @[{self.info.serialize()}]"


@dataclass(frozen=True)
class StringLit(FirrtlNode):
    """Utility Literal Representation"""
    string: str

    def escape(self) -> str:
        return repr(self.string).replace('"', '\\"')

    def serialize(self) -> str:
        return self.escape()[1:-1]


class Expression(FirrtlNode, ABC):
    """EXPRESSIONs"""
    ...


class Type(FirrtlNode, ABC):
    """TYPEs"""
    ...


@dataclass(frozen=True, init=False)
class UnknownType(Type):
    def serialize(self) -> str:
        return '?'


@dataclass(frozen=True)
class Reference(Expression):
    name: str
    typ: Type

    def serialize(self) -> str:
        return self.name


@dataclass(frozen=True)
class SubField(Expression):
    expr: Expression
    name: str
    typ: Type

    def serialize(self) -> str:
        return f"{self.expr.serialize()}.{self.name}"


@dataclass(frozen=True)
class SubIndex(Expression):
    expr: Expression
    value: int
    typ: Type

    def serialize(self) -> str:
        return f"{self.expr.serialize()}[{self.value}]"


@dataclass(frozen=True)
class SubAccess(Expression):
    expr: Expression
    index: Expression
    typ: Type

    def serialize(self) -> str:
        return f"{self.expr.serialize()}[{self.index.serialize()}]"


@dataclass(frozen=True)
class Mux(Expression):
    cond: Expression
    tval: Expression
    fval: Expression
    typ: Type

    def serialize(self) -> str:
        return f"mux({self.cond.serialize()}, {self.tval.serialize()}, {self.fval.serialize()})"


@dataclass(frozen=True)
class DoPrim(Expression):
    op: PrimOp
    args: List[Expression]
    consts: List[int]
    typ: Type

    def serialize(self) -> str:
        sl: List[str] = [arg.serialize() for arg in self.args] + [repr(con) for con in self.consts]
        return f'{self.op.serialize()}({", ".join(sl)})'


@dataclass(frozen=True)
class Width(FirrtlNode, ABC):
    """WIDTH"""


@dataclass(frozen=True)
class IntWidth(Width):
    width: int

    def serialize(self) -> str:
        return f'<{self.width}>'


@dataclass(frozen=True, init=False)
class UnknownWidth(Width):
    width: int = None

    def serialize(self) -> str:
        return ""


@dataclass(frozen=True, init=False)
class UIntLiteral(Expression):
    value: int
    width: Width = UnknownWidth()

    @property
    def typ(self) -> Type:
        return UIntType(self.width)

    def __init__(self, value: int, width: Optional[Width] = None):
        object.__setattr__(self, 'value', value)
        iwidth = width if width is not None else IntWidth(max(value.bit_length(), 1))
        object.__setattr__(self, 'width', iwidth)

    def serialize(self) -> str:
        return f'UInt{self.width.serialize()}("h{hex(self.value)[2:]}")'


@dataclass(frozen=True, init=False)
class SIntLiteral(Expression):
    value: int
    width: Width = UnknownWidth()

    @property
    def typ(self) -> Type:
        return SIntType(self.width)

    def __init__(self, value: int, width: Optional[Width] = None):
        object.__setattr__(self, 'value', value)
        iwidth = width if width is not None else IntWidth(value.bit_length() + 1)
        object.__setattr__(self, 'width', iwidth)

    def serialize(self) -> str:
        return f'SInt{self.width.serialize()}("h{hex(self.value)[2:]}")'


class GroundType(Type, ABC):
    ...


class AggregateType(Type, ABC):
    ...


@dataclass(frozen=True)
class UIntType(GroundType):
    width: Width = UnknownWidth()

    def serialize(self) -> str:
        return f'UInt{self.width.serialize()}'

    def irWithIndex(self, index):
        if isinstance(index, slice):
            length = index.start - index.stop + 1
            return lambda _: {"ir": DoPrim(Bits(), [_], [index.start, index.stop], UIntType(IntWidth(length))),
                              "inNode": True}
        else:
            return lambda _: {"ir": DoPrim(Bits(), [_], [index, index], UIntType(IntWidth(1))),
                              "inNode": True}


@dataclass(frozen=True)
class SIntType(GroundType):
    width: Width = UnknownWidth()

    def irWithIndex(self, index):
        if isinstance(index, slice):
            length = index.start - index.stop + 1
            return lambda _: {"ir": DoPrim(Bits(), [_], [index.start, index.stop], UIntType(IntWidth(length))),
                              "inNode": True}
        else:
            return lambda _: {"ir": DoPrim(Bits(), [_], [index, index], UIntType(IntWidth(1))),
                              "inNode": True}

    def serialize(self) -> str:
        return f'SInt{self.width.serialize()}'


class Orientation(FirrtlNode, ABC):
    """# Orientation of [[Field]]"""
    ...


@dataclass(frozen=True, init=False)
class Default(Orientation):
    def serialize(self) -> str:
        return ''


@dataclass(frozen=True, init=False)
class Flip(Orientation):
    def serialize(self) -> str:
        return 'flip '


@dataclass(frozen=True)
class Field(FirrtlNode):
    """# Field of [[BundleType]]"""
    name: str
    flip: Orientation
    typ: Type

    def serialize(self) -> str:
        return f'{self.flip.serialize()}{self.name} : {self.typ.serialize()}'


@dataclass(frozen=True)
class BundleType(AggregateType):
    fields: List[Field]

    def serialize(self) -> str:
        return '{' + ', '.join([f.serialize() for f in self.fields]) + '}'


@dataclass(frozen=True)
class VectorType(AggregateType):
    typ: Type
    size: int

    def serialize(self) -> str:
        return f'{self.typ.serialize()}[{self.size}]'

    def irWithIndex(self, index):
        if isinstance(index, int):
            return lambda _: {"ir": SubIndex(_, index, self.typ)}
        else:
            return lambda _: {"ir": SubAccess(_, index, self.typ)}


@dataclass(frozen=True)
class MemoryType(AggregateType):
    typ: Type
    size: int

    def serialize(self) -> str:
        return f'{self.typ.serialize()}[{self.size}]'

    def irWithIndex(self, index):
        return lambda _: {"ir": lambda name, mem, clk, rw: DefMemPort(name, mem, index, clk, rw), "inPort": True}


@dataclass(frozen=True, init=False)
class ClockType(GroundType):
    width: Width = IntWidth(1)

    def serialize(self) -> str:
        return 'Clock'


class Direction(FirrtlNode, ABC):
    """[[Port]] Direction"""
    ...


@dataclass(frozen=True, init=False)
class Input(Direction):
    def serialize(self) -> str:
        return 'input'


@dataclass(frozen=True, init=False)
class Output(Direction):
    def serialize(self) -> str:
        return 'output'


# [[DefModule]] Port
@dataclass(frozen=True)
class Port(FirrtlNode):
    name: str
    direction: Direction
    typ: Type
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'{self.direction.serialize()} {self.name} : {self.typ.serialize()}{self.info.serialize()}'


class Statement(FirrtlNode, ABC):
    ...


@dataclass(frozen=True, init=False)
class EmptyStmt(Statement):
    def serialize(self) -> str:
        return 'skip'


@dataclass(frozen=True)
class DefWire(Statement):
    name: str
    typ: Type
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'wire {self.name} : {self.typ.serialize()}{self.info.serialize()}'


@dataclass(frozen=True)
class DefRegister(Statement):
    name: str
    typ: Type
    clock: Expression
    reset: Optional[Expression] = None
    init: Optional[Expression] = None
    info: Info = NoInfo()

    def serialize(self) -> str:
        i: str = indent(f' with : \nreset => ({self.reset.serialize()}, {self.init.serialize()})') \
            if self.init is not None else ""
        return f'reg {self.name} : {self.typ.serialize()}, {self.clock.serialize()}{i}{self.info.serialize()}'


@dataclass(frozen=True)
class DefInstance(Statement):
    name: str
    module: str
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'inst {self.name} of {self.module}{self.info.serialize()}'


# @dataclass(frozen=True)
# class DefMemory(Statement):
#     name: str
#     dataType: Type
#     depth: int
#     writeLatency: int
#     readLatency: int
#     readers: List[str]
#     writers: List[str]
#     readWriters: List[str]
#     readUnderWrite: Optional[str] = None
#     info: Info = NoInfo()
#
#     def serialize(self) -> str:
#         lst = [f"\ndata-type => {self.dataType.serialize()}",
#                f"depth => {self.depth}",
#                f"read-latency => {self.readLatency}",
#                f"write-latency => {self.writeLatency}"] + \
#               [f"reader => {r}" for r in self.readers] + \
#               [f"writer => {w}" for w in self.writers] + \
#               [f"readwriter => {rw}" for rw in self.readWriters] + \
#               ['read-under-write => undefined']
#         s = indent('\n'.join(lst))
#         return f'mem {self.name} :{self.info.serialize()}{s}'

@dataclass(frozen=True)
class DefMemory(Statement):
    name: str
    memType: MemoryType
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'cmem {self.name} : {self.memType.serialize()}{self.info.serialize()}'


@dataclass(frozen=True)
class DefNode(Statement):
    name: str
    value: Expression
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'node {self.name} = {self.value.serialize()}{self.info.serialize()}'


@dataclass(frozen=True)
class DefMemPort(Statement):
    name: str
    mem: Reference
    index: Expression
    clk: Expression
    rw: bool
    info: Info = NoInfo()

    def serialize(self) -> str:
        rw = "read" if self.rw else "write"
        return f'{rw} mport {self.name} = {self.mem.serialize()}[{self.index.serialize()}], ' \
            f'{self.clk.serialize()}{self.info.serialize()}'


@dataclass(frozen=True)
class Conditionally(Statement):
    pred: Expression
    conseq: Statement
    alt: Statement
    info: Info = NoInfo()

    def serialize(self) -> str:
        s = indent(f'\n{self.conseq.serialize()}') + \
            ('' if self.alt == EmptyStmt() else '\nelse :' + indent(f'\n{self.alt.serialize()}'))
        return f'when {self.pred.serialize()} :{self.info.serialize()}{s}'


@dataclass(frozen=True)
class Block(Statement):
    stmts: List[Statement]

    def serialize(self) -> str:
        return '\n'.join([stmt.serialize() for stmt in self.stmts])


@dataclass(frozen=True)
class Connect(Statement):
    loc: Expression
    expr: Expression
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'{self.loc.serialize()} <= {self.expr.serialize()}{self.info.serialize()}'


# Base class for modules
class DefModule(FirrtlNode, ABC):
    def serializeHeader(self, typ: str) -> str:
        ps = indent(''.join([f'\n{p.serialize()}' for p in self.ports]))
        return f'{typ} {self.name} :{self.info.serialize()}{ps}\n'


@dataclass(frozen=True)
class Module(DefModule):
    name: str
    ports: List[Port]
    body: Statement
    typ: BundleType
    info: Info = NoInfo()

    def serialize(self) -> str:
        return self.serializeHeader('module') + indent(f'\n{self.body.serialize()}')


@dataclass(frozen=True)
class ExtModule(DefModule):
    name: str
    ports: List[Port]
    defname: str
    typ: BundleType
    info: Info = NoInfo()

    def serialize(self) -> str:
        s = indent(f'\ndefname = {self.defname}\n')
        return f'{self.serializeHeader("extmodule")}{s}'



@dataclass(frozen=True)
class Circuit(FirrtlNode):
    modules: List[DefModule]
    main: str
    info: Info = NoInfo()

    def serialize(self) -> str:
        ms = '\n'.join([indent(f'\n{m.serialize()}') for m in self.modules])
        return f'circuit {self.main} :{self.info.serialize()}{ms}\n'
