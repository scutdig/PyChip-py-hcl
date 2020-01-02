from enum import Enum
from typing import Dict

from py_hcl.core.type import HclType
from py_hcl.core.type.wrapper import vec_wrap, bd_fld_wrap


class Dir(Enum):
    SRC = 1
    SINK = 2


@bd_fld_wrap
@vec_wrap
class BundleT(HclType):
    def __init__(self, fields: Dict[str, dict]):
        self.type = "bundle"
        self.fields = fields

    # def rev(self):
    #     types = {}
    #     for k, v in self.fields.items():
    #         d = Dir.SINK if v[0] == Dir.SRC else Dir.SRC
    #         types[k] = {dir: d, type: v[1]}
    #     return BundleT(types)
