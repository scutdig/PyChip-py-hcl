from .type_measurer import TypeMeasurer
from .width_measurer import WidthMeasurer
from .field_measurer import FieldMeasurer


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
