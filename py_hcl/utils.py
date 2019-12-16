def signed_num_bin_len(num):
    return len("{:+b}".format(num))


def unsigned_num_bin_len(num):
    return len("{:b}".format(num))


def auto_repr(cls):
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s = %s' % item for item in vars(self).items())
        )

    cls.__repr__ = __repr__
    return cls
