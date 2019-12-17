from multipledispatch import dispatch


def signed_num_bin_len(num):
    return len("{:+b}".format(num))


def unsigned_num_bin_len(num):
    return len("{:b}".format(num))


def auto_repr(cls):
    def __repr__(self):
        ls = ['{}={}'.format(k, _fm(v)) for k, v in vars(self).items()]
        fs = _iter_repr(ls)
        return '%s {%s}' % (type(self).__name__, ''.join(fs))

    cls.__repr__ = __repr__
    return cls


@dispatch()
def _fm(vd: dict):
    ls = ['{}: {}'.format(k, _fm(v)) for k, v in vd.items()]
    fs = _iter_repr(ls)
    return '{%s}' % (''.join(fs))


@dispatch()
def _fm(v: list):
    ls = [_fm(a) for a in v]
    fs = _iter_repr(ls)
    return '[%s]' % (''.join(fs))


@dispatch()
def _fm(v: tuple):
    ls = [_fm(a) for a in v]
    fs = _iter_repr(ls)
    return '(%s)' % (''.join(fs))


@dispatch()
def _fm(v: object):
    return str(v)


def _iter_repr(ls):
    if len(ls) <= 1:
        fs = ''.join(ls)
    else:
        fs = ''.join(['\n  {},'.format(_indent(l)) for l in ls]) + '\n'
    return fs


def _indent(s: str) -> str:
    s = s.split('\n')
    return '\n  '.join(s)
