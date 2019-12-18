from py_hcl.core.stmt.connect import ConnSide


def assert_right_side(f):
    def _(*args):
        check_lists = [a for a in args if hasattr(a, 'conn_side')]
        sides = [ConnSide.RT, ConnSide.BOTH]

        # TODO: Accurate Error Message
        assert all(a.conn_side in sides for a in check_lists)
        return f(*args)

    return _
