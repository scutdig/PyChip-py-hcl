def get_attr(obj, item):
    try:
        return object.__getattribute__(obj, item)
    except AttributeError:
        return None


def has_attr(obj, item):
    if get_attr(obj, item) is None:
        return False
    else:
        return True
