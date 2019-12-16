from multipledispatch import dispatch

from py_hcl.firrtl_ir.type.field import Field

measurer = dispatch


@measurer(Field, Field)
def equal(f1: Field, f2: Field):
    if f1.name != f2.name:
        return False
    if f1.is_flipped != f2.is_flipped:
        return False

    return equal(f1.tpe, f2.tpe)
