from py_hcl.core.type import HclType
from py_hcl.core.type.error import TypeError
from py_hcl.core.type.wrapper import bd_fld_wrap


@bd_fld_wrap
class VectorT(HclType):
    def __init__(self, inner_type: HclType, size: int):
        if size <= 0:
            raise TypeError.size_err(
                f'Vector size can not equal or less than 0, got {size}')

        self.type = "vector"
        self.size = size
        self.inner_type = inner_type
