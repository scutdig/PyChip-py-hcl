from py_hcl.utils import auto_repr


@auto_repr
class HclType(object):
    pass


class UnknownType(HclType):
    pass
