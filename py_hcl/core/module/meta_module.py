from py_hcl.core.expr.mod_inst import con_module
from py_hcl.core.module_factory import packer


class MetaModule(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.__new__ = con_module

        packed = packer.pack(bases, dct, name)
        cls.packed_module = packed
