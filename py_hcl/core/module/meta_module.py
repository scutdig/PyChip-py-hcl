from py_hcl.core.expr.mod_inst import con_module
from py_hcl.core.module_factory import packer
from py_hcl.core.module_factory.error import ModuleError


class MetaModule(type):
    def __init__(cls, name, bases, dct):
        if name == '_hcl_fake_module':
            return

        super().__init__(name, bases, dct)
        cls.__new__ = con_module

        name = fetch_module_name(name)

        check_io_exist(dct, name)
        dct["io"].io_chain_head.io_holder.module_name = name

        packed = packer.pack(bases, dct, name)
        cls.packed_module = packed


module_names = {}


def fetch_module_name(name: str) -> str:
    n = module_names.get(name, 0)
    module_names[name] = n + 1
    return name + ("" if n == 0 else str(n))


def check_io_exist(dct, name):
    if 'io' not in dct:
        raise ModuleError.not_contains_io(
            'module {} lack of io attribute'.format(name))
