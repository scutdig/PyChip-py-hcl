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
        return f"{self.expr.verilog_serialize()}_{self.name}"


@dataclass(frozen=True)
class SubIndex(Expression):
    name: str
    expr: Expression
    value: int
    typ: Type

    def serialize(self) -> str:
        return f"{self.expr.serialize()}[{self.value}]"

    def verilog_serialize(self) -> str:
        return f"{self.expr.verilog_serialize()}_{self.value}"


@dataclass(frozen=True)
class SubAccess(Expression):
    expr: Expression
    index: Expression
    typ: Type

    def serialize(self) -> str:
        return f"{self.expr.serialize()}[{self.index.serialize()}]"

    def verilog_serialize(self):
        sub_access_declares: List[str] = []

        def auto_gen_name(endwith: int):
            if endwith < 0:
                endwith = 0
            return f'_GEN_{endwith}'
        
        def gen_sub_access(s: str, i: str) -> str:
            return f'{auto_gen_name(i)} = {s} : '

        def verilog_serializes(e: Expression):
            # TODO: remove dead code
            conds_rec: List[str] = []
            conds: List[str] = []
            vecs_rec: List[str] = []
            vecs: List[str] = []
            cond_declares: List[str] = []
            vec_declares: List[str] = []
            if type(e.expr) == SubAccess:
                conds_rec, vecs_rec = verilog_serializes(e.expr)
            if type(e.expr.typ) == VectorType:
                typ_size = e.expr.typ.size
                for i in range(typ_size):
                    cond = f'{e.index.verilog_serialize()} == {UIntLiteral(i, IntWidth(get_binary_width(typ_size - 1))).verilog_serialize()}'
                    conds.append(cond)
                    vecs.append(f'{e.expr.name}_{i}') if hasattr(e.expr, 'name') else vecs.append(f'_{i}')

            for c in conds:
                if len(conds_rec) > 0:
                    for cr in conds_rec:
                        cond_declares.append(f'{cr} & {c}')
                else:
                    cond_declares.append(c)
            
            for v in vecs:
                if len(vecs_rec) > 0:
                    for vr in vecs_rec:
                        vec_declares.append(f'{vr}{v}')
                else:
                    vec_declares.append(v)

            return cond_declares, vec_declares

        cond_declares, vec_declares = verilog_serializes(self)
        declares = list(zip(cond_declares, vec_declares))
        count = SubAccessGenCounter.get_count()

        for i in range(count, len(declares) + count):
            cond, vec = declares[i - count]
            sub_access_declare = f'{cond} ? {vec}'
            gsa = gen_sub_access(sub_access_declare, i)
            sub_access_declares.append(f'wire {self.typ.verilog_serialize()} {gsa}{auto_gen_name(i-1)}')
            SubAccessGenCounter.increase()
        
        return '\n'.join(sub_access_declares), auto_gen_name(len(declares) - 1)

@dataclass(frozen=True)
class Mux(Expression):
    cond: Expression
    tval: Expression
    fval: Expression
    typ: Type

    def serialize(self) -> str:
        return f"mux({self.cond.serialize()}, {self.tval.serialize()}, {self.fval.serialize()})"

    def verilog_serialize(self, ext: str = '') -> str:
        return f"{self.cond.verilog_serialize()} ? {self.tval.verilog_serialize()}{ext} : {self.fval.verilog_serialize()}{ext}"
    
@dataclass(frozen=True)
class ValidIf(Expression):
    cond: Expression
    value: Expression
    typ: Type

    def serialize(self) -> str:
        return f"validif({self.cond.serialize()}, {self.value.serialize()})"
    
    def verilog_serialize(self) -> str:
        return f"{self.cond.verilog_serialize()} ? {self.value.verilog_serialize()} : z"


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
        return ""

    def verilog_serialize(self) -> str:
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
        # no "flip" in verilog, bug here
        return 'flip'


@dataclass(frozen=True)
class Field(FirrtlNode):
    """# Field of [[BundleType]]"""
    name: str
    flip: Orientation
    typ: Type

    def serialize(self) -> str:
        return f'{self.flip.serialize()}{self.name} : {self.typ.serialize()}'

    def verilog_serialize(self) -> str:
        return f'{self.flip.verilog_serialize()}{self.typ.verilog_serialize()}\t${self.name}'


@dataclass(frozen=True)
class BundleType(AggregateType):
    fields: List[Field]

    def serialize(self) -> str:
        return '{' + ', '.join([f.serialize() for f in self.fields]) + '}'

    def verilog_serialize(self) -> list:
        # TODO: remove dead code
        field_list = []
        for f in self.fields:
            if type(f.typ) is VectorType:
                vec_declares, typ = f.typ.verilog_serialize()
                for t in vec_declares:
                    field_list.append(f'{typ.verilog_serialize()}\t${f.name}{t}')
            else:
                field_list.append(f.verilog_serialize())
        return field_list


@dataclass(frozen=True)
class VectorType(AggregateType):
    typ: Type
    size: int

    def serialize(self) -> str:
        return f'{self.typ.serialize()}[{self.size}]'

    
    def verilog_serialize(self):
        # TODO: remove dead code
        index_list = []
        in_index_list = []
        if type(self.typ) == VectorType:
            in_index_list, typ = self.typ.verilog_serialize()
        if len(in_index_list) > 0:
            for i in range(self.size):
                for ii in in_index_list:
                    index_list.append(f'_{i}{ii}')
            
            return index_list, typ
        else:
            for i in range(self.size):
                index_list.append(f'_{i}')
            
            return index_list, self.typ

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
        return ""


@dataclass(frozen=True, init=False)
class ResetType(GroundType):
    width: Width = IntWidth(1)

    def serialize(self) -> str:
        return "UInt<1>"

    def verilog_serialize(self) -> str:
        # Todo
        return "Reset"


@dataclass(frozen=True, init=False)
class AsyncResetType(GroundType):
    width: Width = IntWidth(1)

    def serialize(self) -> str:
        return "AsyncReset"

    def verilog_serialize(self) -> str:
        # Todo
        return "AsyncReset"


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
        if type(self.typ.verilog_serialize()) is str:
            return f'{self.direction.verilog_serialize()}\t{self.typ.verilog_serialize()}\t{self.name},\n'
        else:
            portdeclares = ''
            seq = self.typ.verilog_serialize()
            for s in seq:
                ns = s.replace('$', f'{self.name}_')
                if "flip" in ns:
                    ns = ns.replace('flip', "")
                    portdeclares += f'{self.direction.verilog_serialize(True)}\t{ns},\n'
                else:
                    portdeclares += f'{self.direction.verilog_serialize()}\t{ns},\n'
            return portdeclares

class Statement(FirrtlNode, ABC):
    ...


@dataclass(frozen=True, init=False)
class EmptyStmt(Statement):
    def serialize(self) -> str:
        return 'skip'

    def verilog_serialize(self) -> str:
        return '// skip'


@dataclass(frozen=True)
class DefWire(Statement):
    name: str
    typ: Type
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'wire {self.name} : {self.typ.serialize()}{self.info.serialize()}'

    def verilog_serialize(self) -> str:
        if type(self.typ) ==  VectorType:
            wire_declares = ''
            vec_declares, typ = self.typ.verilog_serialize()
            for i in vec_declares:
                wire_declares += f'wire\t{typ.verilog_serialize()}\t{self.name}{i};\n'
            return wire_declares
        return f'wire\t{self.typ.verilog_serialize()}\t{self.name}{self.info.verilog_serialize()};'


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
        return f'reg {self.typ.verilog_serialize()}\t{self.name}{self.info.verilog_serialize()};'


@dataclass(frozen=True)
class DefInstance(Statement):
    name: str
    module: str
    ports: List[Port]
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'inst {self.name} of {self.module}{self.info.serialize()}'

    def verilog_serialize(self) -> str:
        instdeclares = ''
        portdeclares = ''
        ports = InstanceManager._getInstancePorts(self.module)
        for p in ports:
            portdeclares += f'wire\t{p.typ.verilog_serialize()}\t{self.name}_{p.name};\n'
            instdeclares += indent(f'\n.{p.name}({self.name}_{p.name}),')
        return f'{portdeclares}{self.module} {self.name} ({instdeclares[:-1]}\n);'



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
        memorydeclares = ''
        memorydeclares += f'{self.memType.verilog_serialize()}\n'
        # memorydeclares += f'{self.info.verilog_serialize()}\n'
        return memorydeclares


@dataclass(frozen=True)
class DefNode(Statement):
    name: str
    value: Expression
    info: Info = NoInfo()

    def serialize(self) -> str:
        return f'node {self.name} = {self.value.serialize()}{self.info.serialize()}'

    def verilog_serialize(self) -> str:
        return f'wire {self.value.typ.verilog_serialize()} {self.name} = {self.value.verilog_serialize()}{self.info.verilog_serialize()};'


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


# stmt pass will change the conseq and alt
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
        s = indent(f'\n{self.conseq.verilog_serialize()}') + \
            ('' if self.alt == EmptyStmt() else '\nelse' + indent(f'\n{self.alt.verilog_serialize()}'))
        return f'if ({self.pred.verilog_serialize()}) {self.info.verilog_serialize()}{s}'

class ValTracer:
    ...


class RegTracer(ValTracer):
    def __init__(self, reg: DefRegister):
        self.stmt = reg
        self.clock = reg.clock
        self.reset = reg.reset
        self.conds = {}

    def add_cond(self, signal: str, action):
        if signal not in self.conds:
            self.conds[signal] = [action]
        else:
            self.conds[signal].append(action)

    def gen_body(self):
        stmts = []
        final_map = {}
        for k, v in self.conds.items():
            if(k == "default"):
                stmts.append(Block(self.conds[k]))
            else:
                stmts.append(Conditionally(Reference(k, UIntType(IntWidth(1))), Block(self.conds[k]), EmptyStmt()))
        self.body = Block(stmts)

    def gen_always_block(self):
        self.gen_body()
        res =  (f'always @(posedge {self.clock.verilog_serialize()}) begin\n' + \
               deleblankline(indent(f'\n{self.body.verilog_serialize()}')) + \
               f'\nend') if len(self.body.stmts) > 0 else ''
        return res

class MemTracer(ValTracer):
    def __init__(self, mem_port: DefMemPort):
        self.stmt = mem_port
        self.clock = mem_port.clk
        self.rw = mem_port.rw
    
    def get_mem_port(self):
        return self.stmt

    def gen_always_block(self):
        if self.rw:
            return ''
        res = f'always @(posedge {self.clock.verilog_serialize()}) begin' + \
            indent(f'\nif ({self.stmt.mem.name}_{self.stmt.name}_en & {self.stmt.mem.name}_{self.stmt.name}_mask) begin') + \
            indent(f'\n{self.stmt.mem.name}[{self.stmt.mem.name}_{self.stmt.name}_addr] <= {self.stmt.mem.name}_{self.stmt.name}_data;', 2) + \
            indent(f'\nend') + \
            f'\nend'
        return res

class PassManager:
    def __init__(self, target_block):
        self.block = target_block

        self.reg_map = {}

        self.mem_map = {}

        self.define_pass()

    def renew(self):
        return self.stmts_pass(self.block)

    # find out all reg definition and its clock and reset infos
    def define_pass(self):
        reg_tracers = [RegTracer(stmt) for stmt in self.block.stmts if type(stmt) == DefRegister]
        self.reg_map = {x.stmt.name: x for x in reg_tracers}

        mem_tracers = [MemTracer(stmt) for stmt in self.block.stmts if type(stmt) == DefMemPort]
        self.mem_map = {x.stmt.name: x for x in mem_tracers}

    # nest
    def stmts_pass(self, block, signal: str = "default") -> Block:
        if type(block) == EmptyStmt:
            return EmptyStmt()
        if type(block) == Conditionally:
            conseq = self.stmts_pass(block.conseq, block.pred.verilog_serialize())
            alt = self.stmts_pass(block.alt, "!" + block.pred.verilog_serialize())
            return Conditionally(block.pred, conseq, alt, block.info)
        for stmt in block.stmts:
            if type(stmt) == Connect and hasattr(stmt.loc, 'name') and stmt.loc.name in self.reg_map:
                stmt.blocking = False
                self.reg_map[stmt.loc.name].add_cond(signal, stmt)
            elif type(stmt) == Connect and hasattr(stmt.loc, 'name') and stmt.loc.name in self.mem_map:
                stmt.mem = { 'loc': self.mem_map[stmt.loc.name].get_mem_port()}
            elif type(stmt) == Connect and hasattr(stmt.expr, 'name') and stmt.expr.name in self.mem_map:
                stmt.mem = { 'expr': self.mem_map[stmt.expr.name].get_mem_port()}
            elif type(stmt) == Conditionally:
                stmt.conseq = self.stmts_pass(stmt.conseq, stmt.pred.verilog_serialize())
                stmt.alt = self.stmts_pass(stmt.alt, f"!({stmt.pred.verilog_serialize()})")
            elif type(stmt) == DefInstance:
                ...
            else:
                pass
        stmts = [stmt for stmt in block.stmts if self.pass_check(stmt)]
        return Block(stmts) if stmts else EmptyStmt()

    def pass_check(self, stmt):
        return type(stmt) != Conditionally and type(stmt) != Connect \
               or type(stmt) == Connect and hasattr(stmt.loc, 'name') and stmt.loc.name not in self.reg_map \
               or type(stmt) == Conditionally and type(stmt.conseq) != EmptyStmt

    def gen_all_always_block(self):
        res = ""
        for reg, tracer in self.reg_map.items():
            always_block = tracer.gen_always_block()
            if len(always_block) > 0:
                res += f'\n// handle register {reg}'
                res += f'\n{always_block}'
        for mem, tracer in self.mem_map.items():
            always_block = tracer.gen_always_block()
            if len(always_block) > 0:
                if tracer.rw is False:
                    res += f'\n// handle memory port {mem}'
                res += f'\n{tracer.gen_always_block()}'
        return res


@dataclass(frozen=True)
class Block(Statement):
    stmts: List[Statement]

    def serialize(self) -> str:
        return '\n'.join([stmt.serialize() for stmt in self.stmts]) if self.stmts else ""

    def auto_gen_node(self, stmt):
        return isinstance(stmt, DefNode) and stmt.name.startswith("_T")

    def get_name(self, e: Expression) -> str:
        if isinstance(e, (SubIndex, SubField, SubAccess)):
            return self.get_name(e.expr)
        elif isinstance(e, Reference):
            return e.name

    def merge_node_e(self, expr: Expression, node_exp_map: Dict[str, Statement], filter_node: set) -> Expression:
        if isinstance(expr, (UIntLiteral, SIntLiteral)):
            return expr
        elif isinstance(expr, Reference):
            en = self.get_name(expr)
            if en in node_exp_map:
                filter_node.add(en)
                return self.merge_node_e(node_exp_map[en].value, node_exp_map, filter_node)
            else:
                return expr
        elif isinstance(expr, (SubField, SubIndex, SubAccess)):
            return expr
        elif isinstance(expr, Mux):
            return Mux(
                self.merge_node_e(expr.cond, node_exp_map, filter_node),
                self.merge_node_e(expr.tval, node_exp_map, filter_node),
                self.merge_node_e(expr.fval, node_exp_map, filter_node),
                expr.typ)
        elif isinstance(expr, ValidIf):
            return ValidIf(
                self.merge_node_e(expr.cond, node_exp_map, filter_node),
                self.merge_node_e(expr.value, node_exp_map, filter_node),
                expr.typ)
        elif isinstance(expr, DoPrim):
            args = list(map(lambda arg: self.merge_node_e(arg, node_exp_map, filter_node), expr.args))
            return DoPrim(expr.op, args, expr.consts, expr.typ)
        else:
            raise TransformException("Unknown Expression.")
    
    def merge_node_s(self, stmt: Statement, node_exp_map: Dict[str, Statement], filter_node: set) -> Statement:
        if isinstance(stmt, EmptyStmt):
            return stmt
        elif isinstance(stmt, Conditionally):
            return Conditionally(
                self.merge_node_e(stmt.pred, node_exp_map, filter_node),
                self.merge_node_s(stmt.conseq, node_exp_map, filter_node),
                self.merge_node_s(stmt.alt, node_exp_map, filter_node),
                stmt.info)
        elif isinstance(stmt, Block):
            node_exp_map = {**node_exp_map, **{s.name: s for s in stmt.stmts if self.auto_gen_node(s)}}
            stmts = []
            for s in stmt.stmts:
                if isinstance(s, Connect):
                    stmts.append(Connect(
                        self.merge_node_e(s.loc, node_exp_map, filter_node),
                        self.merge_node_e(s.expr, node_exp_map, filter_node),
                        s.info, s.blocking, s.bidirection, s.mem))
                elif isinstance(s, DefNode):
                    stmts.append(DefNode(
                        s.name,
                        self.merge_node_e(s.value, node_exp_map, filter_node),
                        s.info))
                elif isinstance(s, Conditionally):
                    stmts.append(Conditionally(
                        self.merge_node_e(s.pred, node_exp_map, filter_node),
                        self.merge_node_s(s.conseq, node_exp_map, filter_node),
                        self.merge_node_s(s.alt, node_exp_map, filter_node),
                        s.info))
                else:
                    stmts.append(s)
                
            stmts = [s for s in stmts if not (isinstance(s, DefNode) and s.name in filter_node)]
            return Block(stmts)
        else:
            raise TransformException(f"{stmt} is unexpected statement.")

    def verilog_serialize(self) -> str:
        new_body = self.merge_node_s(self, {}, set())
        manager = PassManager(new_body)
        new_blocks = manager.renew()
        # CheckCombLoop.run(new_blocks)
        always_blocks = manager.gen_all_always_block()

        return '\n'.join([stmt.verilog_serialize() for stmt in new_blocks.stmts]) + f'\n{always_blocks}' if new_blocks.stmts else ""


# pass will change the  "blocking" feature of Connect Stmt
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
        if type(self.expr) == SubAccess:
            rec, sub_access = self.expr.verilog_serialize()
            return f'{rec}\nassign {self.loc.verilog_serialize()} {op} {sub_access};'

        for attr, memport in self.mem.items():
            if attr == 'loc':
                return f'assign {memport.mem.name}_{self.loc.verilog_serialize()}_data' + \
                    f' {op} {self.expr.verilog_serialize()}{self.info.verilog_serialize()};'
            if attr == 'expr':
                return f'assign {self.loc.verilog_serialize()}' + \
                    f' {op} {memport.mem.name}_{self.expr.verilog_serialize()}_data{self.info.verilog_serialize()};'
        
        if self.blocking is False:
            return f'{self.loc.verilog_serialize()} {op} {self.expr.verilog_serialize()}{self.info.verilog_serialize()};'
       
        return f'assign {self.loc.verilog_serialize()} {op} {self.expr.verilog_serialize()}{self.info.verilog_serialize()};'


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
        moduledeclares = '  ' + indent(''.join([f'{p.verilog_serialize()}' for p in self.ports]))
        return f'{typ} {self.name}(\n{deleblankline(moduledeclares)[:-1]}\n);\n'


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
        # return f'{self.verilog_serializeHeader("module")}endmodule\n'
        return ''


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
        InstanceManager(self)
        CheckCombLoop()
        SubAccessGenCounter()

class InstanceManager:
    _modules: Dict[str, DefModule] = {}
    _extModules: Dict[str, DefModule] = {}

    def __init__(self, c: Circuit):
        self._c = c
        self._dealExtModules()

    def _dealExtModules(self):
        for m in self._c.modules:
            if isinstance(m, Module):
                InstanceManager._modules[m.name] = m
            if isinstance(m, ExtModule):
                InstanceManager._extModules[m.name] = m
    
    @staticmethod
    def _getInstancePorts(name):
        if name in InstanceManager._modules:
            return InstanceManager._modules[name].ports
        if name in InstanceManager._extModules:
            return InstanceManager._extModules[name].ports

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

class SubAccessGenCounter:
    count = 0

    @staticmethod
    def increase():
        SubAccessGenCounter.count += 1
    
    @staticmethod
    def get_count():
        return SubAccessGenCounter.count
