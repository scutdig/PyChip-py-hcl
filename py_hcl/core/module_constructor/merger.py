from ..module_constructor import module_err


def merge_expr(dest, src):
    io_dest = dest['io']
    io_src = src['io']
    io_dest = merge_io(io_dest, io_src)

    a = set(dest.keys()) & set(src.keys())
    if len(a) > 1:
        raise module_err('DuplicateName')

    res = {**dest, **src, 'io': io_dest}
    return res


def merge_io(dest, src):
    return dest, src  # TODO


def merge_scope(dest, src):
    return dest, src  # TODO
