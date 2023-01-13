import csv
import os

def reduce(func, iterable):
    f = next(iterable)
    s = next(iterable)
    res = func(f, s)
    for item in iterable:
        res = func(res, item)
    return res


def join_tables(path_to_result, paths_to_tables, key):
    all_headers = set()
    big_d = {}
    for path_to_table in paths_to_tables:
        with open(path_to_table, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            all_headers = all_headers | set(reader.fieldnames)
            for row in reader:
                if row[key] not in big_d:
                    big_d[row[key]] = {}
                d = big_d[row[key]]
                d[key] = row[key]
                for head in reader.fieldnames:
                    d[head] = row[head]

    write_file = open(path_to_result, 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(write_file, fieldnames=[key] + list(all_headers - {key}))
    writer.writeheader()
    for d in big_d.values():
        writer.writerow(d)

    write_file.close()

def appends_tables(path_to_result, paths_to_tables):
    with open(path_to_result, 'w', newline='', encoding='utf-8') as write_file:

        with open(paths_to_tables[0], encoding='utf-8') as read_file:
            reader = csv.DictReader(read_file)
            writer = csv.DictWriter(write_file, ['rank'] + list(set(reader.fieldnames) - {''}))
            writer.writeheader()
            writer.writerows([d for d in reader])

        for path_to_table in paths_to_tables[1:]:
            with open(path_to_table, encoding='utf-8') as read_file:
                reader = csv.DictReader(read_file)
                writer.writerows([d for d in reader])



#path = '../static/tables/demand/'
#p = list(map(lambda x: path + x, ['count_by_year.csv', 'salary_by_year.csv', 'selected_count_by_year.csv', 'selected_salary_by_year.csv']))
#join_tables(path + 'compile.csv', p, 'Year')

#path = '../static/tables/geography/'
#p = list(map(lambda x: path + x, ['fraction_by_area.csv', 'salary_by_area.csv']))
#join_tables(path + 'compile.csv', p, 'area_name')


path = '../static/tables/skills/'
os.remove(path + 'compile.csv')
p = [path + i for i in os.listdir(path)]
appends_tables(path + 'compile.csv', p)

