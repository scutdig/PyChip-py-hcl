from dataclasses import dataclass
from typing import Dict, List
from pyhcl.ir.low_ir import *


@dataclass
class AutoInferring:
    max_width: int = 0

    def run(self, c: Circuit):
        modules: List[Module] = []

        def auto_inferring_t(t: Type) -> Type:
            if isinstance(t, UIntType):
                if t.width.width == 0:
                    return UIntType(IntWidth(self.max_width))
                else:
                    self.max_width = self.max_width if self.max_width > t.width.width else t.width.width
                    return t
            elif isinstance(t, SIntType):
                if t.width.width == 0:
                    return SIntType(IntWidth(self.max_width))
                else:
                    self.max_width = self.max_width if self.max_width > t.width.width else t.width.width
                    return t
            elif isinstance(t, (ClockType, ResetType, AsyncResetType)):
                return t
            elif isinstance(t, VectorType):
                return VectorType(auto_inferring_t(t.typ), t.size)
            elif isinstance(t, MemoryType):
                return MemoryType(auto_inferring_t(t.typ), t.size)
            elif isinstance(t, BundleType):
                return BundleType([Field(fx.name, fx.flip, auto_inferring_t(fx.typ)) for fx in t.fields])
            else:
                return t

        def auto_inferring_e(e: Expression, inferring_map: Dict[str, Type]) -> Expression:
            if isinstance(e, Mux):
                return Mux(auto_inferring_e(e.cond, inferring_map), auto_inferring_e(e.tval, inferring_map),
                auto_inferring_e(e.fval, inferring_map), auto_inferring_t(e.typ))
            elif isinstance(e, ValidIf):
                return ValidIf(auto_inferring_e(e.cond, inferring_map), auto_inferring_e(e.value, inferring_map), auto_inferring_t(e.typ))
            elif isinstance(e, DoPrim):
                return DoPrim(e.op, [auto_inferring_e(arg, inferring_map) for arg in e.args], e.consts, auto_inferring_t(e.typ))
            elif isinstance(e, UIntLiteral):
                if e.width.width < get_binary_width(e.value):
                    return UIntLiteral(e.value, IntWidth(get_binary_width(e.value)))
                else:
                    return e
            elif isinstance(e, SIntLiteral):
                if e.width.width < get_binary_width(e.value) + 1:
                    return SIntLiteral(e.value, IntWidth(get_binary_width(e.value)))
                else:
                    return e
            elif isinstance(e, Reference):
                typ = inferring_map[e.name] if inferring_map[e.name] else auto_inferring_t(e.typ)
                return Reference(e.name, typ)
            elif isinstance(e, SubField):
                expr = auto_inferring_e(e.expr, inferring_map)
                typ = e.typ
                for fx in expr.typ.fields:
                    if fx.name == e.name:
                        typ = fx.typ
                return SubField(expr, e.name, typ)
            elif isinstance(e, SubIndex):
                expr = auto_inferring_e(e.expr, inferring_map)
                return SubIndex(e.name, expr, e.value, expr.typ.typ)
            elif isinstance(e, SubAccess):
                expr = auto_inferring_e(e.expr, inferring_map)
                index = auto_inferring_e(e.index, inferring_map)
                return SubAccess(expr, index, expr.typ.typ)
            else:
                return e

        def auto_inferring_s(s: Statement, inferring_map: Dict[str, Type]) -> Statement:
            if isinstance(s, Block):
                stmts: List[Statement] = []
                for sx in s.stmts:
                    stmts.append(auto_inferring_s(sx, inferring_map))
                return Block(stmts)
            elif isinstance(s, Conditionally):
                return Conditionally(auto_inferring_e(s.pred, inferring_map), auto_inferring_s(s.conseq, inferring_map), auto_inferring_s(s.alt, inferring_map), s.info)
            elif isinstance(s, DefRegister):
                clock = auto_inferring_e(s.clock, inferring_map)
                reset = auto_inferring_e(s.reset, inferring_map)
                init = auto_inferring_e(s.init, inferring_map)
                typ = auto_inferring_t(s.typ)
                inferring_map[s.name] = typ
                return DefRegister(s.name, typ, clock, reset, init, s.info)
            elif isinstance(s, DefWire):
                inferring_map[s.name] = auto_inferring_t(s.typ)
                return s
            elif isinstance(s, DefMemory):
                inferring_map[s.name] = auto_inferring_t(s.memType)
                return s
            elif isinstance(s, DefNode):
                value = auto_inferring_e(s.value, inferring_map)
                inferring_map[s.name] = value.typ
                return DefNode(s.name, value, s.info)
            elif isinstance(s, DefMemPort):
                clk = auto_inferring_e(s.clk, inferring_map)
                index = auto_inferring_e(s.index, inferring_map)
                return DefMemPort(s.name, s.mem, index, clk, s.rw, s.info)
            elif isinstance(s, Connect):
                return Connect(auto_inferring_e(s.loc, inferring_map), auto_inferring_e(s.expr, inferring_map), s.info, s.blocking, s.bidirection, s.mem)
            else:
                return s
            

        def auto_inferring_m(m: DefModule, inferring_map: Dict[str, Type]) -> DefModule:
            if isinstance(m, Module):
                ports: List[Port] = []
                for p in m.ports:
                    inferring_map[p.name] = auto_inferring_t(p.typ)
                    ports.append(Port(p.name, p.direction, inferring_map[p.name], p.info))
                body = auto_inferring_s(m.body, inferring_map)
                return Module(m.name, ports, body, m.typ, m.info)
            else:
                return m

        for m in c.modules:
            inferring_map: Dict[str, Type] = {}
            modules.append(auto_inferring_m(m, inferring_map))
        return Circuit(modules, c.main, c.info)