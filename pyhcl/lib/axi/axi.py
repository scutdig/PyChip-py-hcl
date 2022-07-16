from pyhcl import *
from .channel import AxiIOFactory

class AxiliteFactory:
    @classmethod
    def make(cls, aw, dw, master):
        class Master(Module):
            io = AxiIOFactory.make(aw, dw, master=1)
            """
            TODO
            """
        class Slave(Module):
            io = AxiIOFactory.make(aw, dw, master=0)
            """
            TODO
            """


