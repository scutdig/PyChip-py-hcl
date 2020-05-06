from pyhcl.core._repr import Node
from pyhcl.core._utils import get_attr, has_attr


class Pub(Node):
    """
    A Tag Class For Showing The Visibility Of Module's Fields
    """

    def __init__(self, value):
        self.value = value
        self.typ = value.typ

    def __repr__(self):
        value = get_attr(self, "value")
        return "Pub(" + str(value) + ")"

    def __getattribute__(self, item):
        if has_attr(self, item):
            return get_attr(self, item)
        else:
            return getattr(self.public(), item)

    def extractForName(self):
        return get_attr(self, "value")

    def public(self):
        return get_attr(self, "value")

    def mapToIR(self, ctx):
        return self.value.mapToIR(ctx)


class MetaPub(type):
    def __call__(cls, *args, **kwargs):
        # unwrap
        func = lambda x: get_attr(x, 'value') if isinstance(x, Pub) else x

        nArgs = [func(i) for i in args]
        nKwargs = {k: func(v) for k, v in kwargs.items()}
        obj = type.__call__(cls, *nArgs, **nKwargs)

        # rewrap
        return Pub(obj)
