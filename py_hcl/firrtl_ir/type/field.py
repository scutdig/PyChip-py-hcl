from ..utils import serialize_str


class Field(object):
    def __init__(self, name, tpe, is_flipped=False):
        self.name = name
        self.tpe = tpe
        self.is_flipped = is_flipped

    def serialize(self, output):
        if self.is_flipped:
            output.write(b"flip ")
        output.write(serialize_str(self.name))
        output.write(b" : ")
        self.tpe.serialize(output)
