from py_hcl.convertor.convertor import convert


def compile_to_firrtl(module_class, path=None):
    m = convert(module_class.packed_module)

    if path is None:
        path = module_class.packed_module.name + ".fir"

    with open(path, 'wb') as f:
        m.serialize_stmt(f)
