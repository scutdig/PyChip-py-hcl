from py_hcl.core.error import CoreError


def set_up():
    TypeError.append({
        'SizeError': {
            'code': 500,
            'value': TypeError('Specified size is invalid.')
        }
    })


class TypeError(CoreError):
    @staticmethod
    def size_err(msg):
        return TypeError.err('SizeError', msg)


set_up()
