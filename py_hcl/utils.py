from functools import partial

from multipledispatch import dispatch


def signed_num_bin_len(num):
    return len("{:+b}".format(num))


def unsigned_num_bin_len(num):
    return len("{:b}".format(num))


def auto_repr(cls=None, repr_fields=()):
    def _(_cls, _repr_fields):
        def __repr__(self):
            if len(_repr_fields) == 0:
                kv = vars(self)
            else:
                kv = {f: vars(self)[f] for f in _repr_fields}
            ls = ['{}={}'.format(k, _fm(v)) for k, v in kv.items()]
            fs = _iter_repr(ls)
            return '%s {%s}' % (type(self).__name__, ''.join(fs))

        _cls.__repr__ = __repr__
        return _cls

    if cls:
        return _(cls, repr_fields)

    return partial(_, _repr_fields=repr_fields)


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
