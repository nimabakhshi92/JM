import pandas as pd

df = pd.DataFrame([{'a': 'aa1', 'b': 'bb1', 'c': 'cc1'},
                   {'a': 'aa1', 'b': 'bb1', 'c': 'cc2'},
                   {'a': 'aa1', 'b': 'bb2', 'c': 'cc3'},
                   {'a': 'aa1', 'b': 'bb2', 'c': 'cc4'},
                   {'a': 'aa2', 'b': 'bb1', 'c': 'cc5'},
                   {'a': 'aa2', 'b': 'bb1', 'c': 'cc6'},
                   {'a': 'aa2', 'b': 'bb2', 'c': 'cc7'},
                   {'a': 'aa2', 'b': 'bb2', 'c': 'cc8'}
                   ])
e = {'aa1': {'bb1': ['cc1', 'cc2'], 'bb2': ['cc3', 'cc4']},
     'aa2': {'bb1': ['cc5', 'cc6'], 'bb2': ['cc7', 'cc8']},
     }


def nest(df, prev):
    print(prev)
    if len(df.columns) == 1:
        return list(df.iloc[:, 0])
    first_col_name = df.columns[0]
    output = {
        key: nest(df[df[first_col_name] == key].drop(first_col_name, axis=1), prev)
        for key in df[first_col_name].unique()
    }
    return output


d = nest(df, {})
print('ok')
