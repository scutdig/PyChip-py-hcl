from multipledispatch import Dispatcher

op_map = {
    '+': Dispatcher('+'),
    '<<=': Dispatcher('<<='),
    '.': Dispatcher('.'),
    '[i]': Dispatcher('[i]'),
    '[i:j]': Dispatcher('[i:j]'),
    'to_sint': Dispatcher('to_sint'),
    'to_uint': Dispatcher('to_uint'),
    'to_bool': Dispatcher('to_bool'),
}


def op_register(operation):
    return op_map[operation].register


def op_apply(operation):
    def _(*objects):
        types = [type(o.hcl_type) for o in objects if hasattr(o, 'hcl_type')]
        func = op_map[operation].dispatch(*types)

        if func is not None:
            return func(*objects)

        msg = 'No matched functions for types {} while calling operation ' \
              '"{}"'.format([t.__name__ for t in types], operation)

        raise NotImplementedError(msg)

    return _
