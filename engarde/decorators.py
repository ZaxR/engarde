# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division)

import functools
import inspect

import engarde.checks as ck


class BaseDecorator(object):
    CLS_FUNC_MAP = {"IsShape": ck.is_shape,
                    "NoneMissing": ck.none_missing,
                    "Unique": ck.unique,
                    "UniqueIndex": ck.unique_index,
                    "IsMonotonic": ck.is_monotonic,
                    "WithinSet": ck.within_set,
                    "WithinRange": ck.within_range,
                    }

    def __init__(self, enabled=True, **kwargs):
        self.enabled = enabled  # setter to enforce bool would be a lot safer, but challenge w/ decorator
        # self.warn = False ? No - put at func level for all funcs and pass through
        self.__dict__.update(kwargs)

    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            df = f(*args, **kwargs)
            if self.enabled:
                check_func = self.CLS_FUNC_MAP[self.__class__.__name__]
                params = inspect.getfullargspec(check_func).args[1:]  # is_shape_func
                # does not currently warn you if you fed in EXTRA parameters not accepted by check_func
                kwargs = {param: getattr(self, param) for param in params if hasattr(self, param)}
                check_func(df, **kwargs)
            return df
        return decorated


class IsShape(BaseDecorator):
    pass


class NoneMissing(BaseDecorator):
    # how to pass in columns=None as default..?
    # add it to kwargs somehow..?
    pass


class Unique(BaseDecorator):
    # how to pass in columns=None as default..?
    # add it to kwargs somehow..?
    pass


class UniqueIndex(BaseDecorator):
    pass


class IsMonotonic(BaseDecorator):
    # how to pass in defaults..?
    # add it to kwargs somehow..?
    # items=None, increasing=None, strict=False
    pass


class WithinSet(BaseDecorator):
    pass


class WithinRange(BaseDecorator):
    pass


class WithinNStd(BaseDecorator):
    # how to pass in defaults..?
    # add it to kwargs somehow..?
    # n=3
    pass


class HasDtypes(BaseDecorator):
    pass


class OneToMany(BaseDecorator):
    pass


class IsSameAs(BaseDecorator):
    pass


class MultiCheck(BaseDecorator):
    pass


def verify(func, *args, **kwargs):
    """
    Assert that `func(df, *args, **kwargs)` is true.
    """
    return _verify(func, None, *args, **kwargs)


def verify_all(func, *args, **kwargs):
    """
    Assert that all of `func(*args, **kwargs)` are true.
    """
    return _verify(func, 'all', *args, **kwargs)


def verify_any(func, *args, **kwargs):
    """
    Assert that any of `func(*args, **kwargs)` are true.
    """
    return _verify(func, 'any', *args, **kwargs)


def _verify(func, _kind, *args, **kwargs):
    d = {None: ck.verify, 'all': ck.verify_all, 'any': ck.verify_any}
    vfunc = d[_kind]

    def decorate(operation_func):
        @wraps(operation_func)
        def wrapper(*operation_args, **operation_kwargs):
            result = operation_func(*operation_args, **operation_kwargs)
            vfunc(result, func, *args, **kwargs)
            return result
        return wrapper
    return decorate


__all__ = ['is_monotonic', 'is_same_as', 'is_shape', 'none_missing',
           'unique_index', 'within_range', 'within_set', 'has_dtypes',
           'verify', 'verify_all', 'verify_any', 'within_n_std',
           'one_to_many', 'is_same_as', 'multi_check']
