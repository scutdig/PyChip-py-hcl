from enum import Enum
from typing import Dict, Tuple

from py_hcl.core.type import HclType


class Dir(Enum):
    IN = 1
    OUT = 2


class BundleT(HclType):
    def __init__(self, types: Dict[str, Tuple[Dir, HclType]]):
        self.types = types
