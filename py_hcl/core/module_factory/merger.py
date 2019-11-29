from py_hcl.core.module_factory import ModuleError
from py_hcl.dsl.expr.io import IO


def merge_expr(dest, src, mod_names):
    io_dest = dest['io']
    io_src = src['io']
    assert isinstance(io_dest, IO)
    assert isinstance(io_src, IO)
    io_dest = merge_io(io_dest, io_src, mod_names)

    check_dup_mod(dest, src, mod_names)

    res = {**dest, **src, 'io': io_dest}
    return res


def check_dup_mod(dest, src, mod_names):
    a = set(dest.keys()) & set(src.keys())
    a.discard('io')
    if len(a) > 0:
        dest_name = mod_names[0]
        src_name = mod_names[1]
        raise ModuleError.duplicate_name(
            'module {} has duplicates with {} in '
            'module {}'.format(dest_name, list(a), src_name)
        )


def merge_io(dest, src, mod_names):
    check_dup_io(dest, src, mod_names)
    dest.ports.extend(src.ports)

    return dest


def check_dup_io(dest, src, mod_names):
    names = set(p['name'] for p in dest.ports)
    for p in src.ports:
        if p['name'] in names:
            dest_name = mod_names[0]
            src_name = mod_names[1]
            raise ModuleError.duplicate_name(
                'module {} has duplicates with {} in '
                'module {} in io'.format(dest_name, p['name'], src_name)
            )


def merge_scope(dest, src, mod_names):
    dest.statements.extend(src.statements)

    return dest
