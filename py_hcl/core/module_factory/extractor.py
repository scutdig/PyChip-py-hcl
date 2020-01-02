from py_hcl.core.expr import HclExpr


def extract(dct):
    res = {}

    for k, v in dct.items():
        # TODO: check if is source not composed expression
        if isinstance(v, HclExpr):
            res[k] = {"expr_id": v.id}

    return res
