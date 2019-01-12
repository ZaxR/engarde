Engarde
=======

[![Build Status](https: // travis - ci.org / TomAugspurger / engarde.svg)](https: // travis - ci.org / TomAugspurger / engarde)

A python package for defensive data analysis. Inspired by the Engarde library (thanks, Tom Augspurger!).
Documentation is at [readthedocs](http: // engarde.readthedocs.org / en / latest / ).

Dependencies
============

- pandas

Supports python 3.5+

Why?
====

Data are messy.
But, our analysis often depends on certain assumptions about our data
that * should * be invariant across updates to your dataset.
`engarde` is a lightweight way to explicitly state your assumptions
and check that they're * actually * true.

This is especially important when working with flat files like CSV
that aren't bound for a more structured destination(e.g. SQL or HDF5).

Examples
========

There are two main ways of using the library, which correspond to the
two main ways I use pandas: writing small scripts or interactively at
the interpreter.

First, as decorators, which are most useful in `.py` scripts
The basic idea is to  write each step of your ETL process as a function
that takes and returns a DataFrame. These functions can be decorated with
the invariants that should be true at that step in the process.

```python
import engarde.decorators as dc
import numpy as np
import pandas as pd


@dc.none_missing()
def f(df1, df2):
    return df1.add(df2)


df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df2 = pd.DataFrame({"a": [1, np.nan, 3], "b": [4, 5, 6]})

print(f(df, df))  # Success
print(f(df, df2))  # AssertionError: (1, 'a')


@dc.is_shape((1290, 10))
@dc.unique_index
def make_design_matrix('data.csv'):
    out = ...
    return out


```

Second, interactively.
The cleanest way to integrate this is through the[``pipe``](http: // pandas - docs.github.io / pandas - docs - travis / basics.html  # tablewise-function-application) method,
introduced in pandas 0.16.2 (June 2015).

```python
>> > import engarde.checks as ck
>> > (df1.reindex_like(df2)
...     .pipe(ck.unique_index)
...     .cumsum()
...     .pipe(ck.within_range, (0, 100))
...)
```

See Also
========

- [assertr](https://github.com/tonyfischetti/assertr)
- [Validada](https://github.com/jnmclarty/validada)

Roadmap
=======

- Pass tests
	- Bug: underlying func can't take kwargs, because cause error on bad_kwargs check in __itit__
	- MultiCheck is broken
- rewrite readme
- Rename library
- push to github
- Rename funcs
- add to pypi
- add readthedocs
- add travis build server
- class factory
- inherit base class and the functions' docstrings w/ __doc__
- rewrite docs
- Add warn flag to prior funcs(refactor to classes to inherit; polymorphism)
- Improve error message outputs
	- Possibly JSON format
- Add functions for:
  - has_infs,
  - has_neg_infs,
  - has_col_order,
  - has_cols,
  - Add check for object type columns that all values are of a python type (e.g. all str),
  - Check incrementing/complete index
- Demo how to use with read files from csv; write func to import, decorate with dc.funcs
