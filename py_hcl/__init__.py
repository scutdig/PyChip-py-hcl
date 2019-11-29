import logging

logging.basicConfig(format='%(asctime)s %(message)s')


class PyHclError(BaseException):
    errs = {}

    @classmethod
    def append(cls, errs):
        PyHclError.errs[cls] = errs

    @classmethod
    def err(cls, name, msg):
        e = PyHclError.errs[cls][name]
        ev = e['value']

        logging.error("[%d]: %s", e['code'], msg)
        return ev
