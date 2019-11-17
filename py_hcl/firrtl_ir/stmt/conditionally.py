from ..utils import serialize_str
from . import Statement


class Conditionally(Statement):
    def __init__(self, pred_ref, seq, alt):
        self.pred_ref = pred_ref
        self.seq = seq
        self.alt = alt

    def serialize_stmt(self, output, indent):
        output.write(b"when ")
        self.pred_ref.serialize(output)
        output.write(b" :\n")
        indent += 1
        output.write(serialize_str("  " * indent))
        self.seq.serialize_stmt(output, indent)
        output.write(b"\nelse :\n")
        output.write(serialize_str("  " * indent))
        self.alt.serialize_stmt(output, indent)
