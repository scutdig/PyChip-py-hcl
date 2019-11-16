from .type import TypeMeasurer
from .width import WidthMeasurer
from .field import FieldMeasurer

final_map = {
    **TypeMeasurer.measurer_map,
    **WidthMeasurer.measurer_map,
    **FieldMeasurer.measurer_map,
}


def equal(x, y):
    try:
        return final_map[(x.__class__, y.__class__)](x, y)
    except (KeyError, NotImplementedError):
        return False
