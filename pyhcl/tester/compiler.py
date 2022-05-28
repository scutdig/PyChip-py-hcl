from functools import reduce
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.tester.wir import *
from pyhcl.tester.symbol_table import SymbolTable
from pyhcl.tester.exception import TesterException
from pyhcl.tester.utils import DAG

@dataclass(frozen=True)
class TesterCompiler:
    symbol_table: SymbolTable
    dags = {}
    modules = {}

    def gen_dag_nodes(self, name: str, typ: Type):
        if isinstance(typ, (UIntType, SIntType, ClockType, ResetType, AsyncResetType)):
            return [name]
        elif isinstance(typ, VectorType):
            names = []
            pre_names = self.gen_dag_nodes(name, typ.typ)
            for n in pre_names:
                for i in range(typ.size):
                    names.append(f"{n}[{i}]")
            return names
        elif isinstance(typ, MemoryType):
            names = []
            pre_names = self.gen_dag_nodes(name, typ.typ)
            for n in pre_names:
                for i in range(typ.size):
                    names.append(f"{n}[{i}]")
            return names
        elif isinstance(typ, BundleType):
            names = []
            for f in typ.fields:
                pre_names = self.gen_dag_nodes(f.name, f.typ)
                for n in pre_names:
                    names.append(f"{name}.{n}")
            return names
    
    def add_dag_node(self, mname: str, name: str, typ: Type):
        vs = self.gen_dag_nodes(name, typ)
        for v in vs:
            self.dags[mname].add_node_if_not_exists(v)
    
    def add_dag_edge(self, mname: str, ind: Expression, dep: Expression):
        if isinstance(dep, (Reference, SubAccess, SubIndex, SubField)):
            self.dags[mname].add_edge(dep.serialize(), ind.serialize())
        elif isinstance(dep, Mux):
            self.add_dag_edge(mname, ind, dep.tval)
            self.add_dag_edge(mname, ind, dep.fval)
        elif isinstance(dep, ValidIf):
            self.add_dag_edge(mname, ind, dep.value)
        elif isinstance(dep, DoPrim):
            for arg in dep.args:
                self.add_dag_edge(mname, ind, arg)
            

    def gen_working_ir(self, mname: str, names: list, expr: Expression) -> Expression:
        if isinstance(expr, SubField):
            names.append(expr.name)
            e = self.gen_working_ir(mname, names, expr.expr)
            get_func, set_func = e.get_func, e.set_func
            return WSubField(expr,
                lambda table=None: get_func(table),
                lambda s, table=None: set_func(s, table))
        elif isinstance(expr, SubAccess):
            index = self.gen_working_ir(mname, [], expr.index)
            index_get_func = index.get_func
            names.append(index_get_func())
            e = self.gen_working_ir(mname, names, expr.expr)
            get_func, set_func = e.get_func, e.set_func
            return WSubAccess(expr,
                lambda table=None: get_func(table),
                lambda s, table=None: set_func(s, table))
        elif isinstance(expr, SubIndex):
            # size = expr.expr.typ.size-1
            names.append(expr.value)
            e = self.gen_working_ir(mname, names, expr.expr)
            get_func, set_func = e.get_func, e.set_func
            return WSubField(expr,
                lambda table=None: get_func(table),
                lambda s, table=None: set_func(s, table))
        else:
            name = expr.serialize()
            names.append(name)
            if not self.symbol_table.has_symbol(mname, name):
                raise TesterException(f"Module [{mname}] Reference {name} is not declared")
            return WReference(expr,
                lambda table=None: self.symbol_table.get_symbol_value(mname, names, table),
                lambda s, table=None: self.symbol_table.set_symbol_value(mname, names, s, table))
    
    def compile_op(self, op, args, consts):
        if isinstance(op, Add):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) + y.get_value(table), args + consts)
        elif isinstance(op, Sub):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) - y.get_value(table), args + consts)
        elif isinstance(op, Mul):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) * y.get_value(table), args + consts)
        elif isinstance(op, Div):
            return lambda table=None: int(reduce(lambda x, y: x.get_value(table) / y.get_value(table), args + consts))
        elif isinstance(op, Rem):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) % y.get_value(table), args + consts)
        elif isinstance(op, Lt):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) < y.get_value(table), args + consts)
        elif isinstance(op, Leq):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) <= y.get_value(table), args + consts)
        elif isinstance(op, Gt):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) > y.get_value(table), args + consts)
        elif isinstance(op, Geq):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) >= y.get_value(table), args + consts)
        elif isinstance(op, Eq):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) == y.get_value(table), args + consts)
        elif isinstance(op, Neq):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) != y.get_value(table), args + consts)
        elif isinstance(op, Neg):
            return lambda table=None: -(args + consts)[0].get_value(table)
        elif isinstance(op, Not):
            return lambda table=None: not (args + consts)[0].get_value(table)
        elif isinstance(op, And):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) & y.get_value(table), args + consts)
        elif isinstance(op, Or):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) | y.get_value(table), args + consts)
        elif isinstance(op, Xor):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) ^ y.get_value(table), args + consts)
        elif isinstance(op, Shl):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) << y.get_value(table), args + consts)
        elif isinstance(op, Shr):
            return lambda table=None: reduce(lambda x, y: x.get_value(table) >> y.get_value(table), args + consts)
        elif isinstance(op, Bits):
            def bits(args, consts, table=None):
                value = '{:032b}'.format(args[0].get_value(table))
                value = value[::-1]
                value_width = len(value)
                lsb = consts[0].get_value(table) if consts[0].get_value(table) < value_width else 0
                msb = consts[1].get_value(table) if consts[1].get_value(table) < value_width else 0
                value = value[msb: lsb] if lsb > msb else value[lsb]
                return int(value, 2)
            return lambda table=None: bits(args, consts, table)
        elif isinstance(op, Cat):
            def cat(args, table):
                hi = args[0].get_value(table) if isinstance(args[0].get_value(table), str) else bin(args[0].get_value(table))[2:]
                lo = args[1].get_value(table) if isinstance(args[1].get_value(table), str) else bin(args[1].get_value(table))[2:]
                # max_len = len(hi) if len(hi) >= len(lo) else len(lo)
                # hi = '{:032b}'.format(args[0].get_value(table))[-max_len:]
                # lo = '{:032b}'.format(args[1].get_value(table))[-max_len:]
                return hi+lo
            return lambda table=None: cat(args, table)
        elif isinstance(op, (AsUInt, AsSInt)):
            return lambda table=None: int(args[0].get_value(table))
        elif isinstance(op, AsClock):
            return lambda table=None: int(args[0].get_value(table)) % 2
        else:
            return lambda table=None: None

    def compile_e(self, mname: str, expr: Expression) -> Expression:
        if isinstance(expr, (Reference, SubField, SubAccess, SubIndex)):
            names = []
            return self.gen_working_ir(mname, names, expr)
        elif isinstance(expr, DoPrim):
            args = list(map(lambda arg: self.compile_e(mname, arg), expr.args))
            consts = [WInt(const) for const in expr.consts]
            return WDoPrim(expr, self.compile_op(expr.op, args, consts))
        elif isinstance(expr, Mux):
            cond = self.compile_e(mname, expr.cond)
            tval = self.compile_e(mname, expr.tval)
            fval = self.compile_e(mname, expr.fval)
            return WMux(expr, lambda table=None: tval.get_value(table) if cond.get_value(table) else fval.get_value(table))
        elif isinstance(expr, ValidIf):
            cond = self.compile_e(mname, expr.cond)
            value = self.compile_e(mname, expr.value)
            return WValidIf(expr, lambda table=None: value.get_value(table) if cond.get_value(table) else None)
        elif isinstance(expr, UIntLiteral):
            return WUIntLiteral(expr)
        elif isinstance(expr, SIntLiteral):
            return WSIntLiteral(expr)
        else:
            return expr

    def compile_s(self, mname: str, s: Statement) -> Statement:
        if isinstance(s, EmptyStmt):
            return EmptyStmt()
        elif isinstance(s, Conditionally):
            return Conditionally(self.compile_e(mname, s.pred), self.compile_s(mname, s.conseq), self.compile_s(mname, s.alt), s.info)
        elif isinstance(s, Block):
            new_stmts = []
            for stmt in s.stmts:
                new_stmts.append(self.compile_s(mname, stmt))
            return Block(new_stmts)
        elif isinstance(s, DefRegister):
            self.add_dag_node(mname, s.name, s.typ)
            self.symbol_table.set_symbol(mname, s)
            return DefRegister(s.name,
                s.typ,
                self.compile_e(mname, s.clock),
                self.compile_e(mname, s.reset),
                self.compile_e(mname, s.init),
                s.info)
        elif isinstance(s, DefMemory):
            self.add_dag_node(mname, s.name, s.memType)
            self.symbol_table.set_symbol(mname, s)
            return s
        elif isinstance(s, DefInstance):
            for p in self.modules[s.module].ports:
                self.add_dag_node(mname, f"{s.name}.{p.name}", p.typ)
            self.symbol_table.set_symbol(mname, DefInstance(s.name, s.module, self.modules[s.module].ports, s.info))
            return DefInstance(s.name, s.module, self.modules[s.module].ports, s.info)
        elif isinstance(s, DefMemPort):
            return DefMemPort(s.name,
                s.mem,
                self.compile_e(mname, s.index),
                self.compile_e(mname, s.clk),
                s.rw,
                s.info)
        elif isinstance(s, DefWire):
            self.add_dag_node(mname, s.name, s.typ)
            self.symbol_table.set_symbol(mname, s)
            return s
        elif isinstance(s, DefNode):
            self.add_dag_node(mname, s.name, s.value.typ)
            self.add_dag_edge(mname, Reference(s.name, s.value.typ), s.value)
            self.symbol_table.set_symbol(mname, s)
            return DefNode(s.name, self.compile_e(mname, s.value), s.info)
        elif isinstance(s, Connect):
            self.add_dag_edge(mname, s.loc, s.expr)
            return Connect(self.compile_e(mname, s.loc), self.compile_e(mname, s.expr), s.info)
        else:
            return s


    def compile_p(self, mname: str, p: Port):
        self.add_dag_node(mname, p.name, p.typ)
        self.symbol_table.set_symbol(mname, p)
        return p

    def compile_m(self, m: DefModule):
        if isinstance(m, Module):
            self.dags[m.name] = DAG()
            self.symbol_table.set_module(m.name)
            ports = list(map(lambda p: self.compile_p(m.name, p), m.ports))
            body = self.compile_s(m.name, m.body)
            return Module(m.name, ports, body, m.typ, m.info)
        elif isinstance(m, ExtModule):
            self.symbol_table.set_module(m.name)
            ...
    
    def compile(self, c: Circuit):
        for m in c.modules:
            self.modules[m.name] = m
        modules = list(map(lambda m: self.compile_m(m), c.modules))
        return Circuit(modules, c.main, c.info), self.dags