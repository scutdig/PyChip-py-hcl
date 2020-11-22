from typing import Dict, Union, Optional, Tuple, List

from py_hcl.core.expr import HclExpr
from py_hcl.core.expr.error import ExprError
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleDirection, BundleT
from py_hcl.core.utils import module_inherit_mro
from py_hcl.utils.serialization import json_serialize


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
    def __init__(self,
                 named_ports: Dict[str, Union[Input, Output]],
                 module_name: Optional[str] = None):
        self.named_ports = named_ports
        self.module_name = module_name


@json_serialize(
    json_fields=["id", "type", "hcl_type", "variable_type", "io_chain"])
class IO(HclExpr):
    def __init__(self, hcl_type: HclType, io_chain: List[IOHolder]):
        self.type = 'io'
        self.hcl_type = hcl_type
        self.variable_type = VariableType.VALUE
        self.io_chain = io_chain


def io_extend(modules: Tuple[type]):
    """


    """

    modules = module_inherit_mro(modules)

    current_ports = {}
    io_chain = []
    for m in modules[::-1]:
        h = m.io.io_chain[0]
        current_ports.update(h.named_ports)
        io_chain.insert(0, h)

    def _(named_ports: Dict[str, Union[Input, Output]]):
        current_ports.update(named_ports)
        io_chain.insert(0, IOHolder(named_ports))
        return IO(__build_bundle_type_from_ports(current_ports), io_chain)

    return _


def __build_bundle_type_from_ports(
        named_ports: Dict[str, Union[Input, Output]]) -> BundleT:
    fields = {}
    for k, v in named_ports.items():
        if isinstance(v, Input):
            fields[k] = {"dir": BundleDirection.SOURCE, "hcl_type": v.hcl_type}
            continue

        if isinstance(v, Output):
            fields[k] = {"dir": BundleDirection.SINK, "hcl_type": v.hcl_type}
            continue

        raise ExprError.io_value_err(
            "type of '{}' is {}, not Input or Output".format(k, type(v)))

    return BundleT(fields)
