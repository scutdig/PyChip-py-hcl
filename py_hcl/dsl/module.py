from ..core.module_constructor.meta_module import MetaModule
from .expression import Expression


class Module(metaclass=MetaModule):
    io = Expression()  # TODO
    clock = Expression()  # TODO
    reset = Expression()  # TODO
