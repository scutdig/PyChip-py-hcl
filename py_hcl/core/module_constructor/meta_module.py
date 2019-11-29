from .packer import pack


class MetaModule(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        packed = pack(bases, dct, name)
        cls.packed_module = packed
