from py_hcl.core.expr import HclExpr
from py_hcl.core.type.bundle import BundleT


class BundleHolder(HclExpr):
    def __init__(self, hcl_type, conn_side, assoc_value):
        self.hcl_type = hcl_type
        self.conn_side = conn_side

        assert isinstance(hcl_type, BundleT)
        assert set(hcl_type.fields.keys()) == set(assoc_value.keys())
        self.assoc_value = assoc_value
