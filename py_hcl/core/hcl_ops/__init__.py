def undefined(*_):
    raise NotImplementedError()


op_map = {
    '+': undefined,
    '<<=': undefined
}


def hcl_operation(operation):
    def f(func):
        op_map[operation] = func
        return func

    return f
