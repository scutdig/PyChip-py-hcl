from typing import Union

import py_hcl.core.expr.io as cio
import py_hcl.core.module_factory.inherit_chain.io as inherit_io
from py_hcl.core.module.base_module import BaseModule
from py_hcl.core.type import HclType


def IO(**named_ports: Union[cio.Input, cio.Output]) -> cio.IO:
    return inherit_io.io_extend((BaseModule, ))(named_ports)


def Input(hcl_type: HclType) -> cio.Input:
    return cio.Input(hcl_type)


def Output(hcl_type: HclType) -> cio.Output:
    return cio.Output(hcl_type)


def io_extend(*modules: type):
    def _(**named_ports: Union[cio.Input, cio.Output]):
        return inherit_io.io_extend(modules)(named_ports)

    return _
