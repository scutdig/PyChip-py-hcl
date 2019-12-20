from typing import Tuple, List


def module_inherit_mro(modules: Tuple[type]) -> List[type]:
    from py_hcl.core.module.meta_module import MetaModule

    modules = type("_hcl_fake_module", modules, {}).mro()
    modules = [m for m in modules[1:] if isinstance(m, MetaModule)]
    return modules
