from typing import Tuple, Union

from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT, Dir


def Bundle(**named_ports: Union[HclType, Tuple[Dir, HclType]]) -> BundleT:
    t = {k: ((Dir.SRC, v) if isinstance(v, HclType) else v)
         for k, v in named_ports.items()}

    return BundleT(t)
