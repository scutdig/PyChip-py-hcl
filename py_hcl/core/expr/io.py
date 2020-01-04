from typing import Dict, Union, Optional, Tuple

from py_hcl.core.expr import HclExpr
from py_hcl.core.expr.error import ExprError
from py_hcl.core.stmt.connect import ConnSide
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import Dir, BundleT
from py_hcl.core.utils import module_inherit_mro
from py_hcl.utils import json_serialize


@json_serialize
class Input(object):
    def __init__(self, hcl_type: HclType):
        self.port_dir = 'input'
        self.hcl_type = hcl_type


@json_serialize
class Output(object):
    def __init__(self, hcl_type: HclType):
        self.port_dir = 'output'
        self.hcl_type = hcl_type


@json_serialize
class IOHolder(object):
    def __init__(self, named_ports: Dict[str, Union[Input, Output]],
                 module_name: Optional[str] = None):
        self.named_ports = named_ports
        self.module_name = module_name


@json_serialize
class IONode(object):
    def __init__(self, io_holder: IOHolder,
                 next_node: Optional["IOHolder"]):
        self.io_holder = io_holder
        if next_node is not None:
            self.next_node = next_node


@json_serialize(json_fields=["id", "type", "hcl_type",
                             "conn_side", "io_chain_head"])
class IO(HclExpr):
    def __init__(self, hcl_type: HclType, io_chain_head: IONode):
        self.type = 'io'
        self.hcl_type = hcl_type
        self.conn_side = ConnSide.RT
        self.io_chain_head = io_chain_head


def io_extend(modules: Tuple[type]):
    modules = module_inherit_mro(modules)

    current_ports = {}
    io_chain = None
    for m in modules[::-1]:
        h = m.io.io_chain_head.io_holder
        current_ports.update(h.named_ports)
        io_chain = IONode(h, io_chain)

    def _(named_ports: Dict[str, Union[Input, Output]]):
        current_ports.update(named_ports)
        io_chain_head = IONode(IOHolder(named_ports), io_chain)
        return IO(calc_type_from_ports(current_ports), io_chain_head)

    return _


def calc_type_from_ports(named_ports: Dict[str, Union[Input, Output]]):
    types = {}
    for k, v in named_ports.items():
        if isinstance(v, Input):
            types[k] = {"dir": Dir.SRC, "hcl_type": v.hcl_type}
            continue

        if isinstance(v, Output):
            types[k] = {"dir": Dir.SINK, "hcl_type": v.hcl_type}
            continue

        raise ExprError.io_value(
            "type of '{}' is {}, not Input or Output".format(k, type(v)))

    return BundleT(types)
