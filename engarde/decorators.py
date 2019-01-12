# -*- coding: utf-8 -*-
import functools
import inspect

import engarde.checks as ck


class BaseDecorator(object):
    def __init__(self, *args, **kwargs):  # how to take args in decorator..?
        self.enabled = True  # setter to enforce bool would be a lot safer, but challenge w/ decorator
        # self.warn = False ? No - put at func level for all funcs and pass through
        self.params = inspect.getfullargspec(self.check_func).args[1:]

        self.__dict__.update(dict(zip(self.params, args)))
        self.__dict__.update(**kwargs)

    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            df = f(*args, **kwargs)
            if self.enabled:
                kwargs = {k: v for k, v in self.__dict__.items() if k not in ["check_func", "enabled", "params"]}
                self.check_func(df, **kwargs)
            return df
        return decorated


class IsShape(BaseDecorator):
    check_func = staticmethod(ck.is_shape)


class NoneMissing(BaseDecorator):
    check_func = staticmethod(ck.none_missing)


class Unique(BaseDecorator):
    check_func = staticmethod(ck.unique)


class UniqueIndex(BaseDecorator):
    check_func = staticmethod(ck.unique_index)


class IsMonotonic(BaseDecorator):
    check_func = staticmethod(ck.is_monotonic)


class WithinSet(BaseDecorator):
    check_func = staticmethod(ck.within_set)


class WithinRange(BaseDecorator):
    check_func = staticmethod(ck.within_range)


class WithinNStd(BaseDecorator):
    check_func = staticmethod(ck.within_n_std)


class HasDtypes(BaseDecorator):
    check_func = staticmethod(ck.has_dtypes)


class OneToMany(BaseDecorator):
    check_func = staticmethod(ck.one_to_many)


class IsSameAs(BaseDecorator):
    check_func = staticmethod(ck.is_same_as)


class MultiCheck(BaseDecorator):
    check_func = staticmethod(ck.multi_check)


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
        @functools.wraps(operation_func)
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
    def example1(df, n):
        return df.add(n)

    example1(df, 5)  # errors

    # # cheese is a kwarg not accepted by the check function. It's ignored.
    # @IsShape(enabled=False, shape=(4, 2), cheese=True)
    # def example1(df):
    #     return df.add(5)

    @NoneMissing(columns=["a"])
    def example1(df):
        return df.add(5)

    example1(df)  # does not error b/c we disabled out decorator
