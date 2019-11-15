def serialize_num(num):
    return serialize_str(str(num))


def serialize_str(s):
    return bytes(s, 'utf-8')


def signed_num_bin_len(num):
    return len(bin(abs(num))) - 1
