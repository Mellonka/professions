import csv


def reduce(func, iterable):
    f = next(iterable)
    s = next(iterable)
    res = func(f, s)
    for item in iterable:
        res = func(res, item)
    return res


def join_tables(path, paths_to_tables, key):
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

    write_file = open(path, 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(write_file, fieldnames=[key] + list(all_headers - {key}))
    writer.writeheader()
    for d in big_d.values():
        writer.writerow(d)

    write_file.close()


#path = '../static/tables/demand/'
#p = list(map(lambda x: path + x, ['count_by_year.csv', 'salary_by_year.csv', 'selected_count_by_year.csv', 'selected_salary_by_year.csv']))
#join_tables(path + 'compile.csv', p, 'Year')

path = '../static/tables/geography/'
p = list(map(lambda x: path + x, ['fraction_by_area.csv', 'salary_by_area.csv']))
join_tables(path + 'compile.csv', p, 'area_name')

