from py_hcl.dsl.expr import ExprError
from py_hcl.dsl.expr.expression import Expression


class IO(Expression):
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


class Input(Exception):
    def __init__(self, tpe):
        self.tpe = tpe


class Output(Exception):
    def __init__(self, tpe):
        self.tpe = tpe
