from py_hcl.core.type import HclType
from py_hcl.core.type.wrapper import bd_fld_wrap


@bd_fld_wrap
class VectorT(HclType):
    def __init__(self, inner_type: HclType, size: int):
        # TODO: Accurate Error Message
        assert size > 0
        self.type = "vector"
        self.size = size
        self.inner_type = inner_type
