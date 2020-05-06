from pyhcl.core._utils import get_attr


class BundleAccessor:
    def provideBundle(self):
        from pyhcl.dsl.bundle import Bundle
        typ = get_attr(self, "typ")
        if isinstance(typ, Bundle):
            return True, typ
        else:
            return False, None

    def getAttr(self, item):
        return get_attr(self, item)

    def __getattribute__(self, item):
        res = get_attr(self, "getAttr")(item)
        if res is not None:
            return res

        pred, bd = get_attr(self, "provideBundle")()

        if pred:
            from pyhcl.core._repr import SubField
            sf: SubField = getattr(bd, item)
            sf.ref = self
            return sf
        else:
            return None


class VecOps:
    def provideVector(self):
        from pyhcl.dsl.vector import Vec
        if isinstance(self.typ, Vec):
            return True, self.typ
        else:
            return False, None

    def size(self):
        isVec, typ = get_attr(self, "provideVector")()
        if isVec:
            return typ.size
        else:
            raise Exception(f"${self} is not vector type")

    def length(self):
        return self.size()

    def reverse(self):
        from pyhcl.core._repr import ReverseView
        isVec, typ = get_attr(self, "provideVector")()
        if isVec:
            return ReverseView(self, typ)
        else:
            raise Exception(f"${self} is not vector type")

    def flatten(self):
        from pyhcl.dsl.vector import Vec
        from pyhcl.core._repr import FlattenView
        isVec, typ = get_attr(self, "provideVector")()
        if isVec:
            l0v = typ
            l1v = typ.typ
            vt = Vec(l0v.size * l1v.size, l1v.typ)
            return FlattenView(self, vt, l0v.size, l1v.size)
        else:
            raise Exception(f"${self} is not vector type")

    def __iter__(self):
        isVec, typ = get_attr(self, "provideVector")()
        if isVec:
            return iter([self[i] for i in range(typ.size)])

        raise Exception(f"${self} is not vector type")

    def __len__(self):
        return self.size()

    def __reversed__(self):
        return self.reverse()