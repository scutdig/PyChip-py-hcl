from py_hcl.firrtl_ir.type.width import Width


class WidthMeasurer(object):
    measurer_map = {}

    @staticmethod
    def equal(x, y):
        try:
            return WidthMeasurer.measurer_map[(type(x), type(y))](x, y)
        except KeyError:
            raise NotImplementedError((type(x), type(y)))


def measurer(clz, cls):
    def f(func):
        WidthMeasurer.measurer_map[(clz, cls)] = func
        return func

    return f


@measurer(Width, Width)
def _(w1, w2):
    return w1.width == w2.width
