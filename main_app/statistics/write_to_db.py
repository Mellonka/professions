import csv
import sqlite3
from functools import reduce


def get_salary(s_from, s_to, s_currency, published_at, db: sqlite3.Connection, header, cash):
    if (s_to == 0 and s_from == 0) or s_currency == '':
        return None
    year, month = published_at.split('T')[0].split('-')[:2]
    if (year, month) not in cash:
        cursor = db.cursor()
        response = cursor.execute(f"SELECT * FROM currencies WHERE date = '{year}-{month}'").fetchall()[0]
        if len(response) == 0:
            return None
        d = {k: v for k, v in zip(header, response)}
        cash[year, month] = d
    else:
        d = cash[year, month]
    if s_currency not in d or d[s_currency] == '':
        return None
    salary = 0
    count = 0
    if s_from != 0:
        salary += s_from
        count += 1
    if s_to != 0:
        salary += s_to
        count += 1
    if s_currency != 'RUR':
        salary *= float(d[s_currency])
    return int(salary // count)


def create_table(name, fields, db: sqlite3.Connection):
    c = db.cursor()
    c.execute(f'''CREATE TABLE {name} ({reduce(lambda x, y: x + y, fields)})''')
    db.commit()
    c.close()


with sqlite3.connect('statistics.db') as db, open('vacancies_with_skills.csv', encoding='utf-8') as file:
    cursor = db.cursor()
    reader = csv.reader(file)
    header = next(reader)
    new_header = ['name text,', 'key_skills text,', 'salary integer,', 'area_name text,', 'published_at text']
    cursor.execute('drop table vacancies')
    db.commit()
    create_table('vacancies', new_header, db)
    currencies_header = [t[1] for t in cursor.execute('pragma table_info(currencies)').fetchall()]
    cash = {}
    fcf = 0
    for row in reader:
        if len(row) != len(header):
            continue
        salary_from = float(row[2]) if row[2] != '' else 0
        salary_to = float(row[3]) if row[3] != '' else 0
        salary = get_salary(salary_from, salary_to, row[4], row[-1], db, currencies_header, cash)

        if salary == None:
            command = "INSERT INTO vacancies (name, key_skills, area_name, published_at) VALUES (?,?,?,?)"
            info = row[0], row[1], row[5], row[-1].split('T')[0]
        else:
            command = "INSERT INTO vacancies VALUES (?,?,?,?,?)"
            info = row[0], row[1], salary, row[5], row[-1].split('T')[0]
        cursor.execute(command, info)
    db.commit()
