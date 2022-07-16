import dataclasses
import warnings
from os import abort

from pyhcl.dsl.module import MetaBlackBox
from .functions import make_dirs

@dataclasses.dataclass(frozen=True)
class FirrtlModule:
    fircode: str

    def serialize(self) -> str:
        return self.fircode


# Use name as the key, may casue problems
def addfirrtlmodule(bbox: MetaBlackBox, fircode):
    if bbox.__name__ in bbox_firmod_map.keys():
        warnings.warn(f"Bbox {bbox.__name__} have been added before")
        abort()
    bbox_firmod_map[bbox.__name__] = FirrtlModule(fircode)
    return bbox_firmod_map[bbox.__name__]

bbox_firmod_map = {}

def replacewithfirmod(modirs):
    res = {}
    for id, modir in modirs.items():
        if modir.name in bbox_firmod_map.keys():
            res[id] = bbox_firmod_map[modir.name]
        else:
            res[id] = modir
    return res

