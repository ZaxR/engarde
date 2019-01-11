# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division)

import functools
import inspect

import engarde.checks as ck


class BaseDecorator(object):
    # todo: metaclass registration
    CLS_FUNC_MAP = {"IsShape": ck.is_shape,
                    "NoneMissing": ck.none_missing,
                    "Unique": ck.unique,
                    "UniqueIndex": ck.unique_index,
                    "IsMonotonic": ck.is_monotonic,
                    "WithinSet": ck.within_set,
                    "WithinRange": ck.within_range,
                    "WithinNStd": ck.within_n_std,
                    "HasDtypes": ck.has_dtypes,
                    "OneToMany": ck.one_to_many,
                    "IsSameAs": ck.is_same_as,
                    "MultiCheck": ck.multi_check}

    def __init__(self, **kwargs):
        print("In __init__()")
        print(kwargs)
        self.enabled = True  # setter to enforce bool would be a lot safer, but challenge w/ decorator
        # self.warn = False ? No - put at func level for all funcs and pass through
        self.__dict__.update(kwargs)

    def __call__(self, f):
        print("In __call_()")
        print(f)

        @functools.wraps(f)
        def decorated(*args, **kwargs):
            print("In decorated")
            print("Args: ", args)
            print("Kwargs: ", kwargs)
            print("self.__dict__: ", self.__dict__)
            df = f(*args, **kwargs)
            if self.enabled:
                check_func = self.CLS_FUNC_MAP[self.__class__.__name__]
                params = inspect.getfullargspec(check_func).args[1:]
                # Warns if parameters fed to decorator that are not accepted by check_func
                unacceptable_kwargs = [k for k in self.__dict__ if k not in (params + ["enabled"])]
                if any(unacceptable_kwargs):
                    print(f"The following passed kwargs are not accepted by {check_func.__name__}: "
                          f"{', '.join(unacceptable_kwargs)}. Ignoring these kwargs and continuing.")
                kwargs = {param: getattr(self, param) for param in params if hasattr(self, param)}
                print("Args: ", args)
                print("Kwargs: ", kwargs)
                print("self.__dict__: ", self.__dict__)
                check_func(df, **kwargs)
            return df
        return decorated


class IsShape(BaseDecorator):
    pass


class NoneMissing(BaseDecorator):
    pass


class Unique(BaseDecorator):
    pass


class UniqueIndex(BaseDecorator):
    pass


class IsMonotonic(BaseDecorator):
    pass


class WithinSet(BaseDecorator):
    pass


class WithinRange(BaseDecorator):
    pass


class WithinNStd(BaseDecorator):
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


if __name__ == '__main__':
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [4, 5, 6]})

    # cheese is a kwarg not accepted by the check function. It's ignored.
    @IsShape(enabled=True, shape=(4, 2), cheese=True)
    def example1(df):
        return df.add(5)

    example1(df)  # errors

    @IsShape((4, 2))
    def example1(df):
        return df.add(5)

    example1(df)  # errors

    # # cheese is a kwarg not accepted by the check function. It's ignored.
    # @IsShape(enabled=False, shape=(4, 2), cheese=True)
    # def example1(df):
    #     return df.add(5)

    @NoneMissing(columns=["a"])
    def example1(df):
        return df.add(5)

    example1(df)  # does not error b/c we disabled out decorator
