# Demo for automatic connections for two different modules
from pyhcl import *

# Directions



if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(TopModule()), "topmodule.fir")
    Emitter.dumpVerilog(f)
