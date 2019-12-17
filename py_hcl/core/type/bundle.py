from enum import Enum
from typing import Dict, Tuple

from py_hcl.core.type import HclType


class Dir(Enum):
    SRC = 1
    SINK = 2


class BundleT(HclType):
    def __init__(self, types: Dict[str, Tuple[Dir, HclType]]):
        self.types = types

    def rev(self):
        types = {}
        for k, v in self.types.items():
            d = Dir.SINK if v[0] == Dir.SRC else Dir.SRC
            types[k] = (d, v[1])
        return BundleT(types)
