from functools import reduce


def CatBits(*args):
    if len(args) == 1:
        return args[0]
    else:
        from pyhcl.core._repr import Cat
        half = len(args) >> 1
        lf = CatBits(*args[:half])
        rt = CatBits(*args[half:])
        return Cat(lf, rt)


def CatVecL2H(vec):
    return CatBits(*[i for i in OneDimensionalization(vec)])


def CatVecH2L(vec):
    return CatBits(*[i for i in OneDimensionalization(vec).reverse()])


def Sum(vec):
    return reduce(lambda x, y: x + y, vec)


def OneDimensionalization(vec):
    a = vec
    for _ in range(a.typ.lvl - 1):
        a = a.flatten()
    return a


