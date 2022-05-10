from functools import reduce
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.tester.wir import *
from pyhcl.tester.symbol_table import SymbolTable
from pyhcl.tester.exception import TesterException

class TesterCompiler:
    symbol_table: SymbolTable

    def gen_working_ir(self, mname: str, expr: Expression) -> Expression:
        if isinstance(expr, SubField):
            e = self.gen_working_ir(mname, expr.expr)
            get_func, set_func = e.get_func, e.set_func
            return WSubField(expr,
                lambda: get_func()[expr.name],
                lambda s: set_func(s)[expr.name])
        elif isinstance(expr, SubAccess):
            e = self.gen_working_ir(mname, expr.expr)
            index = self.gen_working_ir(mname, expr.index)
            get_func, set_func = e.get_func, e.set_func
            index_get_func = index.get_func
            return WSubAccess(expr,
                lambda: get_func()[index_get_func()],
                lambda s: set_func(s)[index_get_func()])
        elif isinstance(expr, SubIndex):
            e = self.gen_working_ir(mname, expr.expr)
            get_func, set_func = e.get_func, e.set_func
            return WSubField(expr,
                lambda: get_func()[expr.value],
                lambda s: set_func(s)[expr.value])
        else:
            name = expr.serialize()
            if not self.symbol_table.has_symbol(mname, name):
                raise TesterException(f"Module [{mname}] Reference [{expr.serialize()}] is not declared")
            return WReference(expr,
                lambda: self.symbol_table.get_symbol_value(mname, name),
                lambda s: self.symbol_table.set_symbol_value(mname, name, s))
    
    def compile_op(self, op, args, consts):
        if isinstance(op, Add):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() + y.get_value(), vx)
        elif isinstance(op, Sub):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() - y.get_value(), vx)
        elif isinstance(op, Mul):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() * y.get_value(), vx)
        elif isinstance(op, Div):
            vx = args + consts
            return lambda: int(reduce(lambda x, y: x.get_value() / y.get_value(), vx))
        elif isinstance(op, Rem):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() % y.get_value(), vx)
        elif isinstance(op, Lt):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() < y.get_value(), vx)
        elif isinstance(op, Leq):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() <= y.get_value(), vx)
        elif isinstance(op, Gt):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() > y.get_value(), vx)
        elif isinstance(op, Geq):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() >= y.get_value(), vx)
        elif isinstance(op, Eq):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() == y.get_value(), vx)
        elif isinstance(op, Neq):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() != y.get_value(), vx)
        elif isinstance(op, Neg):
            vx = args + consts
            return lambda: -vx[0].get_value()
        elif isinstance(op, Not):
            vx = args + consts
            return lambda: not vx[0].get_value()
        elif isinstance(op, And):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() & y.get_value(), vx)
        elif isinstance(op, Or):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() | y.get_value(), vx)
        elif isinstance(op, Xor):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() ^ y.get_value(), vx)
        elif isinstance(op, Shl):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() << y.get_value(), vx)
        elif isinstance(op, Shr):
            vx = args + consts
            return lambda: reduce(lambda x, y: x.get_value() >> y.get_value(), vx)
        elif isinstance(op, Bits):
            return lambda: int(str(bin(args[0].get_value))[2+consts[0].get_value(): 2+consts[1].get_value()], 2)
        elif isinstance(op, Cat):
            return lambda: int(str(bin(args[0].get_value()))[2:]+str(bin(args[0].get_value()))[2:], 2)
        elif isinstance(op, (AsUInt, AsSInt)):
            return lambda: int(args[0].get_value())
        elif isinstance(op, AsClock):
            return lambda: int(args[0].get_value()) % 2
        else:
            return lambda: None

    def compile_e(self, mname: str, expr: Expression) -> Expression:
        if isinstance(expr, (Reference, SubField, SubAccess, SubIndex)):
            return self.gen_working_ir(mname, expr)
        elif isinstance(expr, DoPrim):
            args = list(map(lambda arg: self.compile_e(mname, arg), expr.args))
            consts = [WInt(const) for const in consts]
            return WDoPrim(expr, self.compile_op(expr.op, args, consts))
        elif isinstance(expr, Mux):
            cond = self.compile_e(mname, expr.cond)
            tval = self.compile_e(mname, expr.tval)
            fval = self.compile_e(mname, expr.fval)
            return WMux(expr, lambda: tval.get_value() if cond.get_value() else fval.get_value())
        elif isinstance(expr, ValidIf):
            cond = self.compile_e(mname, expr.cond)
            value = self.compile_e(mname, expr.value)
            return WValidIf(expr, lambda: value.get_value() if cond.get_value() else None)
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
            return Conditionally(self.compile_e(s.pred), self.compile_s(s.conseq), self.compile_s(s.alt), s.info)
        elif isinstance(s, Block):
            new_stmts = []
            for stmt in s.stmts:
                new_stmts.append(self.compile_s(mname, stmt))
            return Block(new_stmts)
        elif isinstance(s, DefRegister):
            self.symbol_table.set_stmt(mname, s)
            return DefRegister(s.name,
                s.typ,
                self.compile_e(mname, s.clock),
                self.compile_e(mname, s.reset),
                self.compile_e(mname, s.init),
                s.info)
        elif isinstance(s, DefMemory):
            self.symbol_table.set_stmt(mname, s)
            return s
        elif isinstance(s, DefInstance):
            self.symbol_table.set_stmt(mname, s)
            return s
        elif isinstance(s, DefMemPort):
            return DefMemPort(s.name,
                s.mem,
                self.compile_e(s.index),
                self.compile_e(s.clk),
                s.rw,
                s.info)
        elif isinstance(s, DefWire):
            self.symbol_table.set_stmt(mname, s)
            return s
        elif isinstance(s, DefNode):
            self.symbol_table.set_stmt(mname, s)
            return DefNode(s.name, self.compile_e(s.value), s.info)
        elif isinstance(s, Connect):
            return Connect(self.compile_e(s.loc), self.compile_e(s.expr), s.info)
        else:
            return s


    def compile_p(self, mname: str, p: Port):
        self.symbol_table.set_port(mname, p)

    def compile_m(self, m: DefModule):
        if isinstance(m, Module):
            self.symbol_table.set_module(m.name)
            ports = list(map(lambda p: self.compile_p(m.name, p), m.ports))
            body = self.compile_s(m.name, m.body)
            return Module(m.name, ports, body, m.typ, m.info)
        elif isinstance(m, ExtModule):
            self.symbol_table.set_module(m.name)
            ...
    
    def compile(self, c: Circuit):
        modules = list(map(lambda m: self.compile_m(m), c.modules))
        return Circuit(modules, c.main, c.info)