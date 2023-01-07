import csv
import pandas as pd

path = r'../static/csv-files/'


def get_df(filename, drop_none=True, encoding='utf-8-sig'):
    if drop_none:
        return pd.read_csv(path + filename, encoding=encoding).dropna()
    else:
        return pd.read_csv(path + filename, encoding=encoding)


def get_list_of_dict(filename, drop_none=True, encoding='utf-8-sig'):
    with open(path + filename, encoding=encoding) as file:
        reader = csv.reader(file)
        header = next(reader)
        if drop_none:
            return [{k: v for k, v in zip(header, row)} for row in reader if all(row)]
        else:
            return [{k: v for k, v in zip(header, row)} for row in reader]

