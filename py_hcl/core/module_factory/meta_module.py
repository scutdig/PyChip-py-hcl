from . import packer


class MetaModule(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        packed = packer.pack(bases, dct, name)
        cls.packed_module = packed
