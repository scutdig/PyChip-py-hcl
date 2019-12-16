def serialize_num(num):
    return serialize_str(str(num))


def serialize_str(s):
    return bytes(s, 'utf-8')
