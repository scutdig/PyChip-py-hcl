from typing import Dict, Union

from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr import HclExpr, ConnDir
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import Dir, BundleT
from py_hcl.utils import _fm, _indent


class Input(object):
    def __init__(self, hcl_type: HclType):
        self.hcl_type = hcl_type


class Output(object):
    def __init__(self, hcl_type: HclType):
        self.hcl_type = hcl_type


class IO(HclExpr):
    def __init__(self, named_ports: Dict[str, Union[Input, Output]]):
        self.hcl_type = IO.handle_args(named_ports)
        self.conn_dir = ConnDir.BOTH

    @staticmethod
    def handle_args(named_ports):
        types = {}
        for k, v in named_ports.items():
            if isinstance(v, Input):
                types[k] = (Dir.IN, v.hcl_type)
                continue

            if isinstance(v, Output):
                types[k] = (Dir.OUT, v.hcl_type)
                continue

            raise ExprError.io_value(
                "type of '{}' is {}, not Input or Output".format(k, type(v)))

        return BundleT(types)

    def __repr__(self):
        return 'IO {\n' \
               '  conn_dir=%s\n' \
               '  hcl_type=%s\n' \
               '}' % (self.conn_dir, _indent(_fm(self.hcl_type)))
