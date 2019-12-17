from ..utils import serialize_num


class Width(object):
    def __init__(self, width):
        self.width = width

    def serialize(self, output):
        output.write(b"<")
        output.write(serialize_num(self.width))
        output.write(b">")
