from multipledispatch import dispatch

from py_hcl.firrtl_ir.type.width import Width

measurer = dispatch


@measurer(Width, Width)
def equal(w1: Width, w2: Width):
    return w1.width == w2.width
