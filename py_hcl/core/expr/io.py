from typing import Dict, Union

from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.connect import ConnLoc
from py_hcl.core.expr.error import ExprError
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import Dir, BundleT
from py_hcl.utils import auto_repr


class Input(object):
    def __init__(self, hcl_type: HclType):
        self.hcl_type = hcl_type


class Output(object):
    def __init__(self, hcl_type: HclType):
        self.hcl_type = hcl_type


@auto_repr(repr_fields=['hcl_type', 'conn_loc'])
class IO(HclExpr):
    def __init__(self, named_ports: Dict[str, Union[Input, Output]]):
        self.hcl_type = IO.handle_args(named_ports)
        self.conn_loc = ConnLoc.BOTH

    @staticmethod
    def handle_args(named_ports):
        types = {}
        for k, v in named_ports.items():
            if isinstance(v, Input):
                types[k] = (Dir.SRC, v.hcl_type)
                continue

            if isinstance(v, Output):
                types[k] = (Dir.SINK, v.hcl_type)
                continue

            raise ExprError.io_value(
                "type of '{}' is {}, not Input or Output".format(k, type(v)))

        return BundleT(types)
