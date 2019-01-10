##############
#### DEMO ####
##############
import engarde.checks as ck
import engarde.decorators as dc
import numpy as np
import pandas as pd


df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df2 = pd.DataFrame({"a": [1, np.nan, 3, 4], "b": [4, 5, 6, 7]})


@dc.multi_check(checks={ck.none_missing: {"columns": None},
                        ck.is_shape: {"shape": (3, 2)}},
                warn=False)
def add_to_df(df, add_amt=5):
    df = df.add(5)
    return df


add_to_df(df)
print(df)

add_to_df(df2)
print(df2)
