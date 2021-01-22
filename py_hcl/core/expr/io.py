from typing import List

from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type import HclType
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


@json_serialize(
    json_fields=["id", "type", "hcl_type", "variable_type", "io_chain"])
class IO(HclExpr):
    def __init__(self, hcl_type: HclType, io_chain: List["IOHolder"]):
        self.type = 'io'
        self.hcl_type = hcl_type
        self.variable_type = VariableType.ReadOnly
        self.io_chain = io_chain
