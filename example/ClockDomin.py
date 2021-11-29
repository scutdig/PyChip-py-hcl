from pyhcl import *

class A(Module):
    io=IO(
        i=input(Bool),
        o=output(Bool),
        en=input(Bool),
    )

    r0 = RegInit(U.w(1))