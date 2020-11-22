from typing import Tuple, List


def module_inherit_mro(bases: Tuple[type]) -> List[type]:
    """
    Returns modules in method resolution order.

    As we want to handle inherit stuff, the mro is a very basic entry to travel
    the inherit graph.


    Examples
    --------

    >>> from py_hcl import *

    A normal PyHCL module `V`:

    >>> class V(Module):
    ...     io = IO()


    A PyHCL module `W` inheriting `V`:

    >>> class W(V):
    ...     io = io_extend(V)()


    Let's see the bases of `W`:

    >>> W.__bases__
    (<class 'py_hcl.core.utils.V'>,)


    So we can get the mro of its bases via `module_inherit_mro`:

    >>> module_inherit_mro(W.__bases__)
    [<class 'py_hcl.core.utils.V'>,
     <class 'py_hcl.core.module.base_module.BaseModule'>]


    A more complicated case:

    >>> class X(W):
    ...     io = io_extend(W)()

    >>> class Y(V):
    ...     io = io_extend(V)()

    >>> class Z(X, Y):
    ...     io = io_extend(X, Y)()


    To handle expression inheritance or statement inheritance of the module
    `Z`, we can first get the mro of `Z`'s bases:

    >>> module_inherit_mro(Z.__bases__)
    [<class 'py_hcl.core.utils.X'>,
     <class 'py_hcl.core.utils.W'>,
     <class 'py_hcl.core.utils.Y'>,
     <class 'py_hcl.core.utils.V'>,
     <class 'py_hcl.core.module.base_module.BaseModule'>]

    """

    from py_hcl.core.module.meta_module import MetaModule

    # Step 1: Build a fake Python class extending bases.
    #
    # Since `Module`s inherit from `MetaModule`, class construction here will
    # trigger `MetaModule.__init__`. We get around the side effect by adding a
    # conditional early return at the beginning of `MetaModule.__init__`.
    fake_type = type("_hcl_fake_module", bases, {})

    # Step 2: Get the method resolution order of the fake class.
    # Step 3: Filter useless types in the mro.
    modules = [m for m in fake_type.mro()[1:] if isinstance(m, MetaModule)]

    return modules
