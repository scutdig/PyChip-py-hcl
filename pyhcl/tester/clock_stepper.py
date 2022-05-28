from abc import ABC, abstractclassmethod
from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.tester.symbol_table import SymbolTable
from pyhcl.tester.executer import TesterExecuter

class ClockStepper(ABC):
    @abstractclassmethod
    def bump_clock(self):
        ...
    
    @abstractclassmethod
    def run(self):
        ...

    @abstractclassmethod
    def get_cycle_count(self):
        ...
    
    @abstractclassmethod
    def combinational_bump(self):
        ...

class SingleClockStepper(ClockStepper):
    def __init__(self, mname: str, symbol: str, executor: TesterExecuter, table: SymbolTable):
        self.mname: str = mname
        self.clock_symbol: str = symbol
        self.executor: TesterExecuter = executor
        self.table: SymbolTable = table
        self.clock_cycles = 0
        self.combinational_bumps = 0
    
    def handle_name(self, name):
        names = name.split(".")
        names.reverse()
        return names
    
    def bump_clock(self, mname: str, clock_symbol: str, value: int):
        self.table.set_symbol_value(mname, self.handle_name(clock_symbol), value)
        self.clock_cycles += 1
    
    def combinational_bump(self, value: int):
        self.combinational_bumps += value
    
    def get_cycle_count(self):
        return self.clock_cycles
    
    def run(self, steps: int):
        def raise_clock():
            self.table.set_symbol_value(self.mname, self.handle_name(self.clock_symbol), 1)
            self.executor.execute(self.mname)

            self.combinational_bumps = 0

        def lower_clock():
            self.table.set_symbol_value(self.mname, self.handle_name(self.clock_symbol), 0)
            self.combinational_bumps = 0
        
        for _ in range(steps):
            if self.executor.get_inputchange():
                self.executor.execute(self.mname)
            self.clock_cycles += 1

            raise_clock()
            lower_clock()


class MultiClockStepper(ClockStepper):
    # TODO: Add MultiCLockStepper
    ...





