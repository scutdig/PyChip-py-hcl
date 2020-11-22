from py_hcl.utils.serialization import json_serialize


@json_serialize
class HclType(object):
    pass


class UnknownType(HclType):
    pass
