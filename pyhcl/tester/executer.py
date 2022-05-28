from typing import Dict, List
from collections import OrderedDict
from copy import deepcopy
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.tester.compiler import TesterCompiler
from pyhcl.tester.symbol_table import SymbolTable
from pyhcl.tester.clock_stepper import SingleClockStepper

class TesterExecuter:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.symbol_table = SymbolTable()
        self.clock_table = {}
        self.inputchange = False
    

    def handle_name(self, name):
        names = name.split(".")
        names.reverse()
        return names
    
    def get_inputchange(self):
        return self.inputchange
    
    def get_ref_name(self, e: Expression):
        if isinstance(e, SubField):
            return self.get_ref_name(e.expr)
        elif isinstance(e, SubIndex):
            return self.get_ref_name(e.expr)
        elif isinstance(e, SubAccess):
            return self.get_ref_name(e.expr)
        else:
            return e.name
    
    def execute_stmt(self, m: Module, stmt: Statement, table=None):
        if isinstance(stmt, Connect):
            stmt.loc.set_value(stmt.expr.get_value(table), table)
        elif isinstance(stmt, DefNode):
            self.symbol_table.set_symbol_value(m.name, self.handle_name(stmt.name), stmt.value.get_value(table), table)
        elif isinstance(stmt, Block):
            for s in stmt.stmts:
                self.execute_stmt(s, table)
        else:
            ...
    
    def execute_module(self, m: Module, ms: Dict[str, DefModule], table=None):
        execute_stmts = OrderedDict()
        instances = OrderedDict()
        conds = []

        def get_in_port_name(name: str, t: Type, d: Direction) -> List[str]:
            if isinstance(d, Input) and isinstance(t, (UIntType, SIntType, ClockType, ResetType, AsyncResetType)):
                return [name]
            elif isinstance(d, Input) and isinstance(t, (VectorType, MemoryType)):
                names = []
                pnames = get_in_port_name(name, t.typ, d)
                for pn in pnames:
                    for i in range(t.size):
                        names.append(f"{pn}[{i}]")
                return names
            elif isinstance(t, BundleType):
                names = []
                for f in t.fields:
                    pnames = []
                    if isinstance(d, Input) and isinstance(f.flip, Default):
                        pnames += get_in_port_name(f.name, f.typ, d)
                    elif isinstance(d, Output) and isinstance(f.flip, Flip):
                        pnames += get_in_port_name(f.name, f.typ, Input())
                    for pn in pnames:
                        names.append(f"{name}.{pn}")
                return names
            else:
                return []
        
        def get_out_port_name(name: str, t: Type, d: Direction) -> List[str]:
            if isinstance(d, Output) and isinstance(t, (UIntType, SIntType)):
                return [name]
            elif isinstance(d, Output) and isinstance(t, (VectorType, MemoryType)):
                names = []
                pnames = get_in_port_name(name, t.typ, d)
                for pn in pnames:
                    for i in range(t.size):
                        names.append(f"{pn}[{i}]")
                return names
            elif isinstance(t, BundleType):
                names = []
                for f in t.fields:
                    pnames = []
                    if isinstance(d, Output) and isinstance(f.flip, Default):
                        pnames += get_out_port_name(f.name, f.typ, d)
                    elif isinstance(d, Input) and isinstance(f.flip, Flip):
                        pnames += get_out_port_name(f.name, f.typ, Output())
                    for pn in pnames:
                        names.append(f"{name}.{pn}")
                return names
            else:
                return []

        def _deal_stmt(s: Statement):
            if isinstance(s, Block):
                for stmt in s.stmts:
                    _deal_stmt(stmt)
            if isinstance(s, Connect):
                execute_stmts[s.loc.expr.serialize()] = s
            elif isinstance(s, DefNode):
                execute_stmts[s.name] = s
            elif isinstance(s, DefInstance):
                instances[s.name] = s
            elif isinstance(s, Conditionally):
                _deal_stmt(s.conseq)
                _deal_stmt(s.alt)
                conds.append(s)
            else:
                ...

        _deal_stmt(m.body)

        inputs = []
        for p in m.ports:
            inputs += get_in_port_name(p.name, p.typ, p.direction)

        for v in self.dags[m.name].travel_graph(inputs):
            if v in execute_stmts:
               self.execute_stmt(m, execute_stmts[v], table)
        
        while len(conds) > 0:
            cond = conds.pop(0)
            if cond.pred.get_value(table):
                _deal_stmt(cond.conseq)
                for execute_stmt in execute_stmts.values():
                    self.execute_stmt(m, execute_stmt, table)

        for ins in instances:
            ref_module_name = instances[ins].module
            ref_module = ms[ref_module_name]
            ref_table = deepcopy(self.symbol_table.table[ref_module_name])

            module_inputs = []
            for p in ref_module.ports:
                module_inputs += get_in_port_name(p.name, p.typ, p.direction)
            ref_inputs = [f"{ins}.{mi}" for mi in module_inputs]

            for i in range(len(module_inputs)):
                self.symbol_table.set_symbol_value(ref_module_name,
                    self.handle_name(module_inputs[i]),
                    self.symbol_table.get_symbol_value(m.name, self.handle_name(ref_inputs[i])),
                    ref_table)

            self.execute_module(ref_module, ms, ref_table)

            module_outputs = []
            for p in ref_module.ports:
                module_outputs += get_out_port_name(p.name, p.typ, p.direction)
            ref_outputs = [f"{ins}.{mi}" for mi in module_outputs]

            for i in range(len(module_outputs)):
                self.symbol_table.set_symbol_value(m.name,
                    self.handle_name(ref_outputs[i]),
                    self.symbol_table.get_symbol_value(ref_module_name, self.handle_name(module_outputs[i]), ref_table))

            for v in self.dags[m.name].travel_graph(ref_outputs):
                if v in execute_stmts:
                    self.execute_stmt(m, execute_stmts[v], table)
            
            while len(conds) > 0:
                cond = conds.pop(0)
                if cond.pred.get_value(table):
                    _deal_stmt(cond.conseq)
                    for execute_stmt in execute_stmts.values():
                        self.execute_stmt(m, execute_stmt, table)
    
    def init_clock(self, table = None):
        if table is None:
            table = self.symbol_table
        for mname in self.symbol_table:
            if mname not in self.clock_table:
                self.clock_table[mname] = {}
            for symbol in self.symbol_table[mname]:
                self.clock_table[mname][symbol] = SingleClockStepper(mname, symbol, self, table)

    def init_executer(self):
        self.compiler = TesterCompiler(self.symbol_table)
        self.compiled_circuit, self.dags = self.compiler.compile(self.circuit)
        self.init_clock()
    
    def set_value(self, mname: str, name: str, singal: int):
        self.inputchange = True
        self.symbol_table.set_symbol_value(mname, self.handle_name(name), singal)
    
    def get_value(self, mname: str, name: str):
        if self.inputchange:
            self.execute(mname)
            self.inputchange = False
        return self.symbol_table.get_symbol_value(mname, self.handle_name(name))
    
    def step(self, n: int, mname: str):
        if n > 0:
            for name in self.clock_table[mname]:
                self.clock_table[mname][name].run(n)
    
    def execute(self, mname: str):
        ms = {m.name: m for m in self.compiled_circuit.modules}
        m = ms[mname]
        self.execute_module(m, ms)
