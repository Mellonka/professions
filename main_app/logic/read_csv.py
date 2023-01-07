import csv
import pandas as pd
import re
from pathlib import Path
from datetime import datetime

path = Path(__file__).resolve().parent.parent / r'static/csv-files'


def get_df(filename, drop_none=True, encoding='utf-8-sig'):
    if drop_none:
        return pd.read_csv(path / filename, encoding=encoding).dropna()
    else:
        return pd.read_csv(path / filename, encoding=encoding)


def get_list_of_dict(filename, drop_none=True, encoding='utf-8-sig'):
    with open(path / filename, encoding=encoding) as file:
        reader = csv.reader(file)
        header = next(reader)
        if drop_none:
            return [{k: v for k, v in zip(header, row)} for row in reader if all(row)]
        else:
            return [{k: v for k, v in zip(header, row)} for row in reader]

def clear_field(field):
    field = re.sub(r'<[^<>]*>', '', field)
    field = re.sub(r" +", ' ', field).strip()
    return field

def process_field(field, header):
    if header in ['salary_from', 'salary_to']:
        if field == '':
            return 0
        return float(field)
    elif header == 'published_at':
        return datetime.fromisoformat(field)
    else:
        return clear_field(field)


def fill_db(filename, encoding='utf-8-sig'):
    with open(path / filename, encoding=encoding) as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            Vacancy.objects.create(**{k: process_field(v, k) for k, v in zip(header, row)})



