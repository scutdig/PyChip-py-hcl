from py_hcl.core.expr import HclExpr


def extract(dct):
    res = {}

    for k, v in dct.items():
        if isinstance(v, HclExpr):
            res[v.id] = k

    return res
