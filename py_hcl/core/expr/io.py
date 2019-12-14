from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr import HclExpr


class IO(HclExpr):
    def __init__(self, **named_ports):
        self.ports = IO.handle_args(named_ports)

    @staticmethod
    def handle_args(named_ports):
        res = []
        for k, v in named_ports.items():
            if isinstance(v, Input):
                res.append({'name': k, 'direct': 'in', 'tpe': v.tpe})
                continue

            if isinstance(v, Output):
                res.append({'name': k, 'direct': 'out', 'tpe': v.tpe})
                continue

            raise ExprError.io_value(
                "type of '{}' is {}, not Input or Output".format(k, type(v)))

        return res


class Input:
    def __init__(self, tpe):
        self.tpe = tpe


class Output:
    def __init__(self, tpe):
        self.tpe = tpe
