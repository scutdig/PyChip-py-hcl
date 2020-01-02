from enum import Enum

from py_hcl.utils import json_serialize


class ScopeType(Enum):
    TOP = 0
    GROUND = 1
    WHEN = 2
    ELSE_WHEN = 3
    OTHERWISE = 4


@json_serialize
class ScopeInfo(object):
    def __init__(self, scope_id, scope_level, scope_type, tag_object=None):
        self.scope_id = scope_id
        self.scope_level = scope_level
        self.scope_type = scope_type
        if tag_object:
            self.tag_object = tag_object


class ScopeLevelManager(object):
    _next_scope_level = 0

    @classmethod
    def current_level(cls):
        return cls._next_scope_level

    @classmethod
    def expand_level(cls):
        cls._next_scope_level += 1

    @classmethod
    def shrink_level(cls):
        cls._next_scope_level -= 1


class ScopeIdManager(object):
    _next_scope_id = 0

    @classmethod
    def next_id(cls):
        ret = cls._next_scope_id
        cls._next_scope_id += 1
        return ret


class ScopeManager(object):
    scope_list = [
        ScopeInfo(
            # TOP SCOPE which contains all modules
            scope_id=ScopeIdManager.next_id(),
            scope_level=ScopeLevelManager.current_level(),
            scope_type=ScopeType.TOP,
        )
    ]
    scope_id_map = {
        scope_list[0].scope_id: scope_list[0]
    }
    scope_expanding_hooks = []
    scope_shrinking_hooks = []

    @classmethod
    def expand_scope(cls, scope_type, tag_object=None):
        ScopeLevelManager.expand_level()

        current_scope = cls.current_scope()
        next_id = ScopeIdManager.next_id()
        next_scope = ScopeInfo(
            scope_id=next_id,
            scope_level=ScopeLevelManager.current_level(),
            scope_type=scope_type,
            tag_object=tag_object,
        )
        cls.scope_id_map[next_id] = next_scope
        cls.scope_list.append(next_scope)

        for fn in cls.scope_expanding_hooks:
            fn(current_scope, next_scope)

    @classmethod
    def shrink_scope(cls):
        ScopeLevelManager.shrink_level()
        current_scope = cls.scope_list.pop()
        next_scope = cls.current_scope()

        for fn in cls.scope_shrinking_hooks:
            fn(current_scope, next_scope)

    @classmethod
    def current_scope(cls):
        return cls.scope_list[-1]

    @classmethod
    def get_scope_info(cls, sid):
        return cls.scope_id_map[sid]

    @classmethod
    def register_scope_expanding(cls, fn):
        cls.scope_expanding_hooks.append(fn)

    @classmethod
    def register_scope_shrinking(cls, fn):
        cls.scope_shrinking_hooks.append(fn)
