import py_hcl.core.expr.wire as cwr
from py_hcl.core.type import HclType


def Wire(hcl_type: HclType) -> cwr.Wire:
    return cwr.Wire(hcl_type)
