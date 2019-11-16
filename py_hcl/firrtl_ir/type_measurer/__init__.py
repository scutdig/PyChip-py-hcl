from .type import TypeMeasurer
from .width import WidthMeasurer
from .field import FieldMeasurer


def equal(x, y):
    try:
        return TypeMeasurer.equal(x, y)
    except NotImplementedError:
        pass

    try:
        return WidthMeasurer.equal(x, y)
    except NotImplementedError:
        pass

    try:
        return FieldMeasurer.equal(x, y)
    except NotImplementedError:
        pass

    return False
