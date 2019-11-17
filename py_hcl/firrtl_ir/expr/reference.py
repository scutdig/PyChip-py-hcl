from ..utils import serialize_str
from . import Expression


class Reference(Expression):
    def __init__(self, name, tpe):
        self.name = name
        self.tpe = tpe

    def serialize(self, output):
        output.write(serialize_str(self.name))
