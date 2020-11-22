from py_hcl.transformer.pyhcl_to_firrtl.convertor import convert


def compile_to_firrtl(module_class, path=None):
    """
    Compiles PyHCL Module `module_class` to FIRRTL source code file.

    Examples
    --------

    Define a PyHCL module:

    >>> from py_hcl import *
    >>> class N(Module):
    ...     io = IO(
    ...         i=Input(U.w(8)),
    ...         o=Output(U.w(8)),
    ...     )
    ...     io.o <<= io.i

    Compile to FIRRTL:

    >>> from tempfile import mktemp
    >>> tmp_file = mktemp()
    >>> compile_to_firrtl(N, tmp_file)

    Read the content:

    >>> with open(tmp_file) as f:
    ...     print(f.read())
    circuit N :
      module N :
        input clock : Clock
        input reset : UInt<1>
        input N_io_i : UInt<8>
        output N_io_o : UInt<8>
    <BLANKLINE>
        N_io_o <= N_io_i
    <BLANKLINE>
    <BLANKLINE>

    >>> from os import remove
    >>> remove(tmp_file)
    """

    m = convert(module_class.packed_module)

    if path is None:
        path = module_class.packed_module.name + ".fir"

    with open(path, 'wb') as f:
        m.serialize_stmt(f)
        f.flush()
