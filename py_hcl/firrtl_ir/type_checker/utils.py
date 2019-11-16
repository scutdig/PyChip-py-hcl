from ..type import UIntType, SIntType


def type_in(obj, *types):
    for t in types:
        if isinstance(obj, t):
            return True
    return False


def all_the_same(*objects):
    t = objects[0]
    for o in objects[1:]:
        if o != t:
            return False
    return True


def check_all_same_uint_sint(*types):
    for t in types:
        if not type_in(t, UIntType, SIntType):
            return False

    return all_the_same(*list(map(type, types)))
