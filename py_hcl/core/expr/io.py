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
