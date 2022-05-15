from pyhcl.tester.executer import TesterExecuter
from pyhcl.ir.low_ir import *
from pyhcl.dsl.emitter import Emitter

class Tester:
    def __init__(self, c: Circuit):
        ec = Emitter.elaborate(c)
        self.main = ec.main
        self.executer = TesterExecuter(ec)
        self.executer.init_executer()
    
    def peek(self, name: str, value: int):
        self.executer.set_value(self.main, name, value)
    
    def poke(self, name: str):
        print(self.executer.get_value(self.main, name))

    def step(self):
        self.executer.execute(self.main)