from py_hcl.utils import json_serialize


@json_serialize
class HclType(object):
    pass


class UnknownType(HclType):
    pass
