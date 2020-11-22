from py_hcl.compile import compile_to_firrtl
from py_hcl.core import install_ops
from py_hcl.core.expr.io import io_extend
from py_hcl.core.module.meta_module import MetaModule

install_ops()


class BaseModule(metaclass=MetaModule):
    io = io_extend(tuple())({})

    @classmethod
    def compile_to_firrtl(cls, path=None):
        """
        Compiles current PyHCL Module to FIRRTL source code file.

        Examples
        --------

        Define a PyHCL module:

        >>> from py_hcl import *
        >>> class M(Module):
        ...     io = IO(
        ...         i=Input(U.w(8)),
        ...         o=Output(U.w(8)),
        ...     )
        ...     io.o <<= io.i

        Compile to FIRRTL:

        >>> from tempfile import mktemp
        >>> tmp_file = mktemp()
        >>> M.compile_to_firrtl(tmp_file)

        Read the content:

        >>> with open(tmp_file) as f:
        ...     print(f.read())
        circuit M :
          module M :
            input clock : Clock
            input reset : UInt<1>
            input M_io_i : UInt<8>
            output M_io_o : UInt<8>
        <BLANKLINE>
            M_io_o <= M_io_i
        <BLANKLINE>
        <BLANKLINE>

        >>> from os import remove
        >>> remove(tmp_file)
        """

        compile_to_firrtl(cls, path)
