import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import sqlite3
import tkinter

def save_df_as_plot(df, path, x_key, y_key):
    plt.rc('font', size=20)
    fig = plt.figure()
    fig.set_figheight(9)
    fig.set_figwidth(9)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.grid(axis='y')
    ax1.bar(df[x_key], df[y_key])
    ax1.tick_params(axis='x', labelrotation=45)
    fig.savefig(path)


def save_plots(salary_by_year, selected_salary_by_year):
    plt.rc('font', size=20)
    fig = plt.figure()
    fig.set_figheight(9)
    fig.set_figwidth(15)
    ax = fig.add_subplot(1, 1, 1)

    d = {k: v for k, v in
         zip(selected_salary_by_year['Year'].to_list(), selected_salary_by_year['avg_salary_for_selected'].to_list())}
    y2 = [d[k] if k in d else 0 for k in salary_by_year['Year'].to_list()]

    ax.bar([i - 0.2 for i in list(map(int, salary_by_year['Year'].to_list()))], salary_by_year['avg_salary'], width=0.4)
    ax.bar([i + 0.2 for i in list(map(int, salary_by_year['Year'].to_list()))], y2, width=0.4)
    ax.set_xticks(list(map(int, salary_by_year['Year'].to_list())))
    ax.tick_params(axis='x', labelrotation=60)
    ax.legend(['средняя з/п', 'средняя з/п для iOS-разработчиков'])
    ax.grid(axis='y')
    fig.savefig('../static/plots/diff_salary.png')

vacancy_name = input()
matplotlib.use('TkAgg')
db = sqlite3.connect('statistics.db')
c = db.cursor()

salary_by_year = pd.read_sql("SELECT strftime('%Y', published_at) as Year, ROUND(AVG(salary)) as avg_salary FROM vacancies WHERE salary is not null GROUP BY strftime('%Y', published_at)", db)
salary_by_year.to_csv('../static/tables/salary_by_year.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(salary_by_year, '../static/plots/salary_by_year.png', 'Year', 'avg_salary')


count_by_year = pd.read_sql("SELECT strftime('%Y', published_at) as Year, COUNT(name) as count_vacancies FROM vacancies GROUP BY strftime('%Y', published_at)", db)
count_by_year.to_csv('../static/tables/count_by_year.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(count_by_year, '../static/plots/count_by_year.png', 'Year', 'count_vacancies')


selected_salary_by_year = pd.read_sql(f"SELECT strftime('%Y', published_at) as Year, ROUND(AVG(salary)) as avg_salary_for_selected FROM vacancies WHERE salary is not null AND LOWER(name) LIKE '%{vacancy_name.lower()}%' GROUP BY strftime('%Y', published_at)", db)
selected_salary_by_year.to_csv('../static/tables/selected_salary_by_year.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(selected_salary_by_year, '../static/plots/selected_salary_by_year.png', 'Year', 'avg_salary_for_selected')


selected_count_by_year = pd.read_sql(f"SELECT strftime('%Y', published_at) as Year, COUNT(name) as count_vacancies_for_selected FROM vacancies WHERE LOWER(name) LIKE '%{vacancy_name.lower()}%' GROUP BY strftime('%Y', published_at)", db)
selected_count_by_year.to_csv('../static/tables/selected_count_by_year.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(selected_count_by_year, '../static/plots/selected_count_by_year.png', 'Year', 'count_vacancies_for_selected')


len_table = int(c.execute("SELECT COUNT(*) FROM vacancies WHERE salary is not null ").fetchall()[0][0])

salary_by_area = pd.read_sql(f"SELECT area_name, ROUND(AVG(salary)) as avg_salary FROM vacancies WHERE salary is not null GROUP BY area_name HAVING COUNT(name) >= {len_table // 100} ORDER BY avg_salary DESC LIMIT 10", db)
salary_by_area.to_csv('../static/tables/salary_by_area.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(salary_by_area, '../static/plots/salary_by_area.png', 'area_name', 'avg_salary')


fraction_by_area = pd.read_sql(f"SELECT area_name, ROUND(COUNT(salary) / {len_table}.0, 3) as fraction_vacancies FROM vacancies GROUP BY area_name HAVING COUNT(name) >= {len_table // 100} ORDER BY fraction_vacancies DESC LIMIT 10", db)
fraction_by_area.to_csv('../static/tables/fraction_by_area.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(fraction_by_area, '../static/plots/fraction_by_area.png', 'area_name', 'fraction_vacancies')

save_plots(salary_by_year, selected_salary_by_year)
