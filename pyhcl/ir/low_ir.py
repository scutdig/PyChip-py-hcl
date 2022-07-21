from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from pyhcl.ir.low_node import FirrtlNode
from pyhcl.ir.low_prim import PrimOp, Bits, Cat
from pyhcl.ir.utils import backspace, indent, deleblankline, backspace1, get_binary_width, TransformException, DAG
class Info(FirrtlNode, ABC):
    """INFOs"""
    def serialize(self) -> str:
        """default implementation"""
        return self.__repr__()

    def verilog_serialize(self) -> str:
        return self.__repr__()

class NoInfo(Info):
    def serialize(self) -> str:
        return ""

    def verilog_serialize(self) -> str:
        return ""

@dataclass(frozen=True)
class FileInfo(Info):
    info: StringLit

    def serialize(self) -> str:
        return f"@[{self.info.serialize()}]"

    def verilog_serialize(self) -> str:
        return f" /*[{self.info.verilog_serialize()}]*/"


@dataclass(frozen=True)
class StringLit(FirrtlNode):
    """Utility Literal Representation"""
    string: str

    def escape(self) -> str:
        return repr(self.string).replace('"', '\\"')

    def serialize(self) -> str:
        return self.escape()[1:-1]

    def verilog_serialize(self) -> str:
        return self.serialize()


class Expression(FirrtlNode, ABC):
    """EXPRESSIONs"""
    ...


class Type(FirrtlNode, ABC):
    """TYPEs"""
    def map_type(self, typ):
        ...
    
    def map_width(self, typ):
        ...


@dataclass(frozen=True, init=False)
class UnknownType(Type):
    def serialize(self) -> str:
        return '?'

    def verilog_serialize(self) -> str:
        return self.serialize()

@dataclass(frozen=True)
class Reference(Expression):
    name: str
    typ: Type

    def serialize(self) -> str:
        return self.name

    def verilog_serialize(self) -> str:
        return self.serialize()


@dataclass(frozen=True)
class SubField(Expression):
    expr: Expression
    name: str
    typ: Type

    def serialize(self) -> str:
        return f"{self.expr.serialize()}.{self.name}"

    def verilog_serialize(self) -> str:
        return self.serialize()


@dataclass(frozen=True)
class SubIndex(Expression):
    name: str
    expr: Expression
    value: int
    typ: Type

    def serialize(self) -> str:
        return f"{self.expr.serialize()}[{self.value}]"

    def verilog_serialize(self) -> str:
        return self.serialize()


@dataclass(frozen=True)
class SubAccess(Expression):
    expr: Expression
    index: Expression
    typ: Type

    def serialize(self) -> str:
        return f"{self.expr.serialize()}[{self.index.serialize()}]"

    def verilog_serialize(self):
        return self.serialize()

@dataclass(frozen=True)
class Mux(Expression):
    cond: Expression
    tval: Expression
    fval: Expression
    typ: Type

    def serialize(self) -> str:
        return f"mux({self.cond.serialize()}, {self.tval.serialize()}, {self.fval.serialize()})"

    def verilog_serialize(self) -> str:
        return f"{self.cond.verilog_serialize()} ? {self.tval.verilog_serialize()} : {self.fval.verilog_serialize()}"
    
@dataclass(frozen=True)
class ValidIf(Expression):
    cond: Expression
    value: Expression
    typ: Type

    def serialize(self) -> str:
        return f"validif({self.cond.serialize()}, {self.value.serialize()})"
    
    def verilog_serialize(self) -> str:
        return f"{self.cond.verilog_serialize()} ? {self.value.verilog_serialize()} : Z"


@dataclass(frozen=True)
class DoPrim(Expression):
    op: PrimOp
    args: List[Expression]
    consts: List[int]
    typ: Type

    def serialize(self) -> str:
        sl: List[str] = [arg.serialize() for arg in self.args] + [repr(con) for con in self.consts]
        return f'{self.op.serialize()}({", ".join(sl)})'

    def verilog_serialize(self) -> str:
        sl: List[str] = [arg.verilog_serialize() for arg in self.args] + [repr(con) for con in self.consts]
        if isinstance(self.op, Cat):
            return f'{{{", ".join(sl)}}}'
        elif isinstance(self.op, Bits):
            arg = self.args[0]
            msb, lsb = self.consts[0], self.consts[1]
            msb_lsb = f'{msb}: {lsb}' if msb != lsb else f'{msb}'
            return f'{arg.verilog_serialize()}[{msb_lsb}]'
        
        if len(sl) > 1:
            return f'{self.op.verilog_serialize().join(sl)}'
        else:
           return f'{self.op.verilog_serialize()}{sl.pop()}'


@dataclass(frozen=True)
class Width(FirrtlNode, ABC):
    """WIDTH"""


@dataclass(frozen=True)
class IntWidth(Width):
    width: int

    def serialize(self) -> str:
        return f'<{self.width}>'

    def verilog_serialize(self) -> str:
        return f'[{self.width - 1}:0]' if self.width - 1 else ""

    def verilog_literal_serialize(self) -> str:
        return str(self.width)


@dataclass(frozen=True, init=False)
class UnknownWidth(Width):
    width: int = None

    def serialize(self) -> str:
        return ''

    def verilog_serialize(self) -> str:
        return ''


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

    def verilog_serialize(self) -> str:
        return f'{self.width.verilog_literal_serialize()}\'h{hex(self.value)[2:]}'


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

    def verilog_serialize(self) -> str:
        return f'{self.width}\'h{hex(self.value)}'


class GroundType(Type, ABC):
    ...


class AggregateType(Type, ABC):
    ...


@dataclass(frozen=True)
class UIntType(GroundType):
    width: Width = UnknownWidth()

    def serialize(self) -> str:
        return f'UInt{self.width.serialize()}'

    def verilog_serialize(self) -> str:
        return f'{self.width.verilog_serialize()}'

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

    def verilog_serialize(self) -> str:
        return f'{self.width.serialize()}'


class Orientation(FirrtlNode, ABC):
    """# Orientation of [[Field]]"""
    ...


@dataclass(frozen=True, init=False)
class Default(Orientation):
    def serialize(self) -> str:
        return ''

    def verilog_serialize(self) -> str:
        return ''


@dataclass(frozen=True, init=False)
class Flip(Orientation):
    def serialize(self) -> str:
        return 'flip '

    def verilog_serialize(self) -> str:
        return ''


@dataclass(frozen=True)
class Field(FirrtlNode):
    """# Field of [[BundleType]]"""
    name: str
    flip: Orientation
    typ: Type

    def serialize(self) -> str:
        return f'{self.flip.serialize()}{self.name} : {self.typ.serialize()}'

    def verilog_serialize(self) -> str:
        return ''


@dataclass(frozen=True)
class BundleType(AggregateType):
    fields: List[Field]

    def serialize(self) -> str:
        return '{' + ', '.join([f.serialize() for f in self.fields]) + '}'

    def verilog_serialize(self) -> list:
        return ''


@dataclass(frozen=True)
class VectorType(AggregateType):
    typ: Type
    size: int

    def serialize(self) -> str:
        return f'{self.typ.serialize()}[{self.size}]'

    
    def verilog_serialize(self):
        return ''

    def irWithIndex(self, index):
        if isinstance(index, int):
            return lambda _: {"ir": SubIndex('', _, index, self.typ)}
        else:
            return lambda _: {"ir": SubAccess(_, index, self.typ)}


@dataclass(frozen=True)
class MemoryType(AggregateType):
    typ: Type
    size: int

    def serialize(self) -> str:
        return f'{self.typ.serialize()}[{self.size}]'

    def verilog_serialize(self) -> str:
        return f'reg {self.typ.verilog_serialize()} m [0:{self.size-1}];'

    def irWithIndex(self, index):
        return lambda _: {"ir": lambda name, mem, clk, rw: DefMemPort(name, mem, index, clk, rw), "inPort": True}


@dataclass(frozen=True, init=False)
class ClockType(GroundType):
    width: Width = IntWidth(1)

    def serialize(self) -> str:
        return 'Clock'

    def verilog_serialize(self) -> str:
        return ''


@dataclass(frozen=True, init=False)
class ResetType(GroundType):
    width: Width = IntWidth(1)

    def serialize(self) -> str:
        return "UInt<1>"

    def verilog_serialize(self) -> str:
        return ''


@dataclass(frozen=True, init=False)
class AsyncResetType(GroundType):
    width: Width = IntWidth(1)

    def serialize(self) -> str:
        return "AsyncReset"

    def verilog_serialize(self) -> str:
        return ''


class Direction(FirrtlNode, ABC):
    """[[Port]] Direction"""
    ...


@dataclass(frozen=True, init=False)
class Input(Direction):
    def serialize(self) -> str:
        return 'input'

    def verilog_serialize(self, flip=False) -> str:
        if flip is True:
            return 'output'
        return 'input'


@dataclass(frozen=True, init=False)
class Output(Direction):
    def serialize(self) -> str:
        return 'output'

    def verilog_serialize(self, flip=False) -> str:
        if flip is True:
            return 'input'
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

    def verilog_serialize(self) -> str:
        return f'{self.direction.verilog_serialize()}\t{self.typ.verilog_serialize()}\t{self.name},\t{self.info.verilog_serialize()}'

class Statement(FirrtlNode, ABC):
    ...


@dataclass(frozen=True, init=False)
class EmptyStmt(Statement):
    def serialize(self) -> str:
        return 'skip'

    def verilog_serialize(self) -> str:
        return ''


@dataclass(frozen=True)
class DefWire(Statement):
    name: str
    typ: Type
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'wire {self.name} : {self.typ.serialize()}{self.info.serialize()}'

    def verilog_serialize(self) -> str:
        return f'wire\t{self.typ.verilog_serialize()}\t{self.name};\t{self.info.verilog_serialize()}'


@dataclass(frozen=True)
class DefRegister(Statement):
    name: str
    typ: Type
    clock: Expression
    reset: Optional[Expression] = None
    init: Optional[Expression] = None
    info: Info = NoInfo()

    def serialize(self) -> str:
        if self.init:
            i: str = indent(f' with : \nreset => ({self.reset.serialize()}, {self.init.serialize()})') \
                if self.init is not None else ""
        else:
            i: str = indent(f' with : \nreset => ({self.reset.serialize()})') \
                if self.reset is not None else ""
        return f'reg {self.name} : {self.typ.serialize()}, {self.clock.serialize()}{i}{self.info.serialize()}'

    def verilog_serialize(self) -> str:
        return f'reg\t{self.typ.verilog_serialize()}\t{self.name};\t{self.info.verilog_serialize()}'

@dataclass(frozen=True)
class DefInstance(Statement):
    name: str
    module: str
    ports: List[Port]
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'inst {self.name} of {self.module}{self.info.serialize()}'

    def verilog_serialize(self) -> str:
        instdeclares: List[str] = []
        portdeclares: List[str] = []
        for p in self.ports:
            portdeclares.append(f'wire\t{p.typ.verilog_serialize()}\t{self.name}_{p.name};')
            instdeclares.append(indent(f'\n.{p.name}({self.name}_{p.name}),'))
        port_decs = '\n'.join(portdeclares)
        return f"{port_decs}\n{self.module}\t{self.name}(\t{self.info.verilog_serialize()}{''.join(instdeclares)});"

@dataclass(frozen=True)
class WDefMemory(Statement):
    name: str
    memType: MemoryType
    dataType: Type
    depth: int
    writeLatency: int
    readLatency: int
    readers: List[str]
    writers: List[str]
    readUnderWrite: Optional[str] = None
    info: Info = NoInfo()

    def serialize(self) -> str:
        lst = [f"\ndata-type => {self.dataType.serialize()}",
               f"depth => {self.depth}",
               f"read-latency => {self.readLatency}",
               f"write-latency => {self.writeLatency}"] + \
              [f"reader => {r}" for r in self.readers] + \
              [f"writer => {w}" for w in self.writers] + \
              ['read-under-write => undefined']
        s = indent('\n'.join(lst))
        return f'mem {self.name} :{self.info.serialize()}{s}'
    
    def verilog_serialize(self) -> str:
        return self.memType.verilog_serialize()

@dataclass(frozen=True)
class DefMemory(Statement):
    name: str
    memType: MemoryType
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'cmem {self.name} : {self.memType.serialize()}{self.info.serialize()}'

    def verilog_serialize(self) -> str:
        return f'{self.memType.verilog_serialize()}\t{self.info.verilog_serialize()}'


@dataclass(frozen=True)
class DefNode(Statement):
    name: str
    value: Expression
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'node {self.name} = {self.value.serialize()}{self.info.serialize()}'

    def verilog_serialize(self) -> str:
        return f'wire\t{self.value.typ.verilog_serialize()}\t{self.name} = {self.value.verilog_serialize()};\t{self.info.verilog_serialize()}'


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

    def verilog_serialize(self) -> str:
        memportdeclares = ''
        memportdeclares += f'wire {self.mem.typ.typ.verilog_serialize()} {self.mem.verilog_serialize()}_{self.name}_data;\n'
        memportdeclares += f'wire [{get_binary_width(self.mem.typ.size)-1}:0] {self.mem.verilog_serialize()}_{self.name}_addr;\n'
        memportdeclares += f'wire {self.mem.verilog_serialize()}_{self.name}_en;\n'
        memportdeclares += f'assign {self.mem.verilog_serialize()}_{self.name}_addr = {get_binary_width(self.mem.typ.size)}\'h{self.index.value};\n'
        memportdeclares += f'assign {self.mem.verilog_serialize()}_{self.name}_en = 1\'h1;\n'
        if self.rw is False:
            memportdeclares += f'wire {self.mem.verilog_serialize()}_{self.name}_mask;\n'
        return memportdeclares

@dataclass(frozen=False)
class Conditionally(Statement):
    pred: Expression
    conseq: Statement
    alt: Statement
    info: Info = NoInfo()

    def serialize(self) -> str:
        s = indent(f'\n{self.conseq.serialize()}') + \
            ('' if self.alt == EmptyStmt() else '\nelse :' + indent(f'\n{self.alt.serialize()}'))
        return f'when {self.pred.serialize()} :{self.info.serialize()}{s}'


    def verilog_serialize(self) -> str:
        s = indent(f"\n{self.conseq.verilog_serialize()}") + "\nend" + \
            ("" if self.alt == EmptyStmt() else "\nelse begin" + indent(f"\n{self.alt.verilog_serialize()}") + "\nend")
        return f"if ({self.pred.verilog_serialize()}) begin\t{self.info.verilog_serialize()}{s}"

@dataclass(frozen=True)
class Block(Statement):
    stmts: List[Statement]

    def serialize(self) -> str:
        return '\n'.join([stmt.serialize() for stmt in self.stmts]) if self.stmts else ""

    def verilog_serialize(self) -> str:
        CheckCombLoop.run(self)
        return '\n'.join([stmt.verilog_serialize() for stmt in self.stmts])

@dataclass(frozen=True)
class AlwaysBlock(Statement):
    stmts: List[Statement]
    clk: Expression = None

    def serialize(self) -> str:
        pass

    def verilog_serialize(self) -> str:
        cat_table: List[str] = []
        for stmt in self.stmts:
            cat_table.append(stmt.verilog_serialize())
        
        if self.clk is None:
            declares = '\n' + "\n".join(cat_table)
            return deleblankline(f"always @(posedge clock) begin\n{indent(declares)}"+ "\nend")
        else:
            declares = '\n' + "\n".join(cat_table)
            return deleblankline(f"always @(posedge {self.clk.verilog_serialize()}) begin\n{indent(declares)}" + "\nend")

@dataclass(frozen=False)
class Connect(Statement):
    loc: Expression
    expr: Expression
    info: Info = NoInfo()
    blocking: bool = True
    bidirection: bool = False
    mem: Dict = field(default_factory=dict)

    def serialize(self) -> str:
        if not self.bidirection:
            return f'{self.info.serialize()}{self.loc.serialize()} <= {self.expr.serialize()}'
        else:
            return f'{self.info.serialize()}\n{self.loc.serialize()} <= {self.expr.serialize()}\n' + \
                   f'{self.info.serialize()}\n{self.expr.serialize()} <= {self.loc.serialize()}'

    def verilog_serialize(self) -> str:
        op = "=" if self.blocking else "<="
        if self.blocking is False:
            return f'{self.loc.verilog_serialize()} {op} {self.expr.verilog_serialize()};\t{self.info.verilog_serialize()}'
        return f'assign\t{self.loc.verilog_serialize()} {op} {self.expr.verilog_serialize()};\t{self.info.verilog_serialize()}'


# Verification
class Verification(FirrtlNode, ABC):
    pass


@dataclass(frozen=True)
class Assert(Verification):
    clk: Expression
    pred: Expression
    en: Expression
    msg: str

    def serialize(self) -> str:
        return f'assert({self.clk.serialize()}, {self.pred.serialize()}, {self.en.serialize()}, \"{self.msg}\")\n'

    def verilog_serialize(self) -> str:
        return ""


@dataclass(frozen=True)
class Assume(Verification):
    clk: Expression
    pred: Expression
    en: Expression
    msg: str

    def serialize(self) -> str:
        return f'assert({self.clk.serialize()}, {self.pred.serialize()}, {self.en.serialize()},{self.msg})\n'

    def verilog_serialize(self) -> str:
        return ""


@dataclass(frozen=True)
class Cover(Verification):
    clk: Expression
    pred: Expression
    en: Expression
    msg: str

    def serialize(self) -> str:
        return f'assert({self.clk.serialize()}, {self.pred.serialize()}, {self.en.serialize()},{self.msg})\n'

    def verilog_serialize(self) -> str:
        return ""


# Base class for modules
class DefModule(FirrtlNode, ABC):
    def serializeHeader(self, typ: str) -> str:
        moduledeclares = indent(''.join([f'\n{p.serialize()}' for p in self.ports]))
        return f'{typ} {self.name} :{self.info.serialize()}{moduledeclares}\n'

    def verilog_serializeHeader(self, typ: str) -> str:
        port_declares: List[str] = []
        for p in self.ports:
            port_declares.append(indent("\n"+  p.verilog_serialize()))
        return f"{typ} {self.name}(\t{self.info.verilog_serialize()}{''.join(port_declares)}\n);\n"


@dataclass(frozen=True)
class Module(DefModule):
    name: str
    ports: List[Port]
    body: Statement
    typ: BundleType
    info: Info = NoInfo()

    def serialize(self) -> str:
        return self.serializeHeader('module') + indent(f'\n{self.body.serialize()}')

    def verilog_serialize(self) -> str:
        return self.verilog_serializeHeader('module') + indent(f'\n{self.body.verilog_serialize()}') + '\nendmodule'


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

    def verilog_serialize(self) -> str:
        return ""


@dataclass(frozen=True)
class Circuit(FirrtlNode):
    modules: List[DefModule]
    main: str
    info: Info = NoInfo()

    def serialize(self) -> str:
        CheckCombLoop()
        ms = '\n'.join([indent(f'\n{m.serialize()}') for m in self.modules])
        return f'circuit {self.main} :{self.info.serialize()}{ms}\n'

    def verilog_serialize(self) -> str:
        self.requires()
        ms = ''.join([f'{m.verilog_serialize()}\n' for m in self.modules])
        return ms
    
    def requires(self):
        CheckCombLoop()

class CheckCombLoop:
    connect_graph = DAG()
    reg_map = {}

    @staticmethod
    def run(stmt: Statement):
        def check_comb_loop_e(u: Expression, v: Expression):
            if isinstance(u, (Reference, SubField, SubIndex, SubAccess)):
                ux, vx = u.serialize(), v.serialize()
                if ux in CheckCombLoop.reg_map or vx in CheckCombLoop.reg_map:
                    return
                try:
                    CheckCombLoop.connect_graph.add_node_if_not_exists(vx)
                    CheckCombLoop.connect_graph.add_node_if_not_exists(ux)
                    CheckCombLoop.connect_graph.add_edge(ux, vx)
                except TransformException as e:
                    raise e
            elif isinstance(u, Mux):
                check_comb_loop_e(u.tval, v)
                check_comb_loop_e(u.fval, v)
            elif isinstance(u, ValidIf):
                check_comb_loop_e(u.value, v)
            elif isinstance(u, DoPrim):
                for arg in u.args:
                    check_comb_loop_e(arg, v)
            else:
                ...

        def check_comb_loop_s(s: Statement):
            if isinstance(s, Connect):
                if isinstance(s.loc, (Reference, SubField, SubIndex, SubAccess)):
                    check_comb_loop_e(s.expr, s.loc)
            elif isinstance(s, DefNode):
                check_comb_loop_e(s.value, Reference(s.name, s.value.typ))
            elif isinstance(s, Conditionally):
                check_comb_loop_s(s.conseq)
                check_comb_loop_s(s.alt)
            elif isinstance(s, EmptyStmt):
                ...
            elif isinstance(s, Block):
                for stmt in s.stmts:
                    check_comb_loop_s(stmt)

        def get_reg_map(s: Statement):
            if isinstance(s, Block):
                for sx in s.stmts:
                    if isinstance(sx, DefRegister):
                        CheckCombLoop.reg_map[sx.name] = sx
                    elif isinstance(sx, DefMemPort):
                        CheckCombLoop.reg_map[f"{sx.mem.name}_{sx.name}_data"] = DefWire(f"{sx.mem.name}_{sx.name}_data",
                            UIntType(IntWidth(sx.mem.typ.size)))
                        CheckCombLoop.reg_map[f"{sx.mem.name}_{sx.name}_addr"] = DefWire(f"{sx.mem.name}_{sx.name}_addr",
                            UIntType(IntWidth(get_binary_width(sx.mem.typ.size))))
                        CheckCombLoop.reg_map[f"{sx.mem.name}_{sx.name}_en"] = DefWire(f"{sx.mem.name}_{sx.name}_en",
                            UIntType(IntWidth(1)))
                        if sx.rw is False:
                            CheckCombLoop.reg_map[f"{sx.mem.name}_{sx.name}_mask"] = DefWire(f"{sx.mem.name}_{sx.name}_mask",
                                UIntType(IntWidth(1)))
                    else:
                        ...
            elif isinstance(s, EmptyStmt):
                ...
            elif isinstance(s, Conditionally):
                get_reg_map(s.conseq)
                get_reg_map(s.alt)

        get_reg_map(stmt)
        check_comb_loop_s(stmt)

        return stmt
