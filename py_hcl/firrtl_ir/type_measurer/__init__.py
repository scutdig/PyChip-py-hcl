from multipledispatch import dispatch

from .type import equal
from .width import equal
from .field import equal

measurer = dispatch


@measurer(object, object)
def equal(_0: object, _1: object):
    return False
