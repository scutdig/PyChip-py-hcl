from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass

@dataclass
class ExpandAggregate(Pass):
    def run(self, c: Circuit) -> Circuit:
        modules: List[DefModule] = []

        def flip_direction(d: Direction) -> Direction:
            if isinstance(d, Output):
                return Input()
            else:
                return Output()

        def flatten_vector(name: str, t: Type) -> list:
            decs = []
            if isinstance(t, VectorType):
                for nx, tx in [(f"{name}_{i}", t.typ) for i in range(t.size)]:
                    if isinstance(tx, VectorType):
                        decs = decs + flatten_vector(nx, tx)
                    elif isinstance(tx, BundleType):
                        decs = decs + [(nxx, txx) for nxx, _, txx in flatten_bundle(nx, tx)]
                    else:
                        decs.append((nx, tx))
            return decs
        
        def flatten_bundle(name: str, t: Type) -> list:
            decs = []
            if isinstance(t, BundleType):
                for nx, fx, tx in [(f"{name}_{f.name}", f.flip, f.typ) for f in t.fields]:
                    if isinstance(tx, BundleType):
                        decs = decs + flatten_bundle(nx, tx)
                    elif isinstance(tx, VectorType):
                        decs = decs + [(nxx, fx, txx) for nxx, txx in flatten_vector(nx, tx)]
                    else:
                        decs.append((nx, fx, tx))
            return decs

        def expand_aggregate(stmt: Statement, stmts: List[Statement]):
            if isinstance(stmt.typ, VectorType):
                typs = flatten_vector(stmt.name, stmt.typ)
                for nx, tx in typs:
                    stmts.append(DefWire(nx, tx, stmt.info))
            elif isinstance(stmt.typ, BundleType):
                typs = flatten_bundle(stmt.name, stmt.typ)
                for nx, _, tx in typs:
                    stmts.append(DefWire(nx, tx, stmt.info))
            else:
                stmts.append(stmt)

        def expand_aggregate_s(stmts: List[Statement]) -> List[Statement]:
            new_stmts = []
            for stmt in stmts:
                if isinstance(stmt, DefWire):
                    expand_aggregate(stmt, new_stmts)
                else:
                    new_stmts.append(stmt)
            return new_stmts

        def expand_aggregate_p(p: Port, ports: List[Port]):
            if isinstance(p.typ, VectorType):
                typs = flatten_vector(p.name, p.typ)
                for nx, tx in typs:
                    ports.append(Port(nx, p.direction, tx, p.info))
            elif isinstance(p.typ, BundleType):
                typs = flatten_bundle(p.name, p.typ)
                for nx, fx, tx in typs:
                    dir = p.direction if isinstance(fx, Default) else flip_direction(p.direction)
                    ports.append(Port(nx, dir, tx, p.info))
            else:
                ports.append(p)

        def expand_aggregate_ps(ps: List[Port]) -> List[Port]:
            new_ports = []
            for p in ps:
                expand_aggregate_p(p, new_ports)
            return new_ports

        def expand_aggregate_m(m: DefModule) -> DefModule:
            if isinstance(m, ExtModule):
                return m
            if not hasattr(m, 'body') or not isinstance(m.body, Block):
                return m
            if not hasattr(m.body, 'stmts') or not isinstance(m.body.stmts, list):
                return m
            
            return Module(m.name, expand_aggregate_ps(m.ports), Block(expand_aggregate_s(m.body.stmts)), m.typ, m.info)

        for m in c.modules:
            modules.append(expand_aggregate_m(m))
        return Circuit(modules, c.main, c.info)