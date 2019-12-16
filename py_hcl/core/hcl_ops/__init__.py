from multipledispatch import Dispatcher

op_map = {
    '+': Dispatcher('+'),
    '<<=': Dispatcher('<<='),
    '.': Dispatcher('.')
}


def hcl_operation(operation):
    return op_map[operation].register


def hcl_call(operation):
    def _(*objects):
        types = [type(o.hcl_type) for o in objects if hasattr(o, 'hcl_type')]
        func = op_map[operation].dispatch(*types)
        return func(*objects)

    return _
