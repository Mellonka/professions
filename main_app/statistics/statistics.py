import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import sqlite3
import numpy as np
import tkinter

def save_df_as_plot(df, path, x_key, y_key):
    plt.rc('font', size=20)
    fig = plt.figure()
    plt.subplots_adjust(top=1)
    fig.set_figheight(12)
    fig.set_figwidth(12)
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(axis='y')
    ax.bar(df[x_key], df[y_key])
    ax.tick_params(axis='x', labelrotation=45)

    # увидел на каком то сайте просто. другого способа пока не нашёл
    for label in ax.get_xticklabels():
        if x_key != 'Year':
            label.set_fontsize(12)

    fig.savefig(path)


def save_plots(bigger_df, smaller_df, general_column, column_bigger_df, column_smaller_df, path, legend=None):
    plt.rc('font', size=20)
    fig = plt.figure()
    fig.set_figheight(9)
    fig.set_figwidth(15)
    ax = fig.add_subplot(1, 1, 1)

    d = {k: v for k, v in
         zip(smaller_df[general_column].to_list(), smaller_df[column_smaller_df].to_list())}
    y2 = [d[k] if k in d else 0 for k in bigger_df[general_column].to_list()]

    ax.bar([i - 0.2 for i in list(map(int, bigger_df[general_column].to_list()))], bigger_df[column_bigger_df], width=0.4)
    ax.bar([i + 0.2 for i in list(map(int, bigger_df[general_column].to_list()))], y2, width=0.4)
    ax.set_xticks(list(map(int, bigger_df[general_column].to_list())))
    ax.tick_params(axis='x', labelrotation=60)
    ax.legend(legend)
    ax.grid(axis='y')
    plt.subplots_adjust(top=1)
    fig.savefig(path)

vacancy_name = 'ios'#input()
matplotlib.use('TkAgg')
db = sqlite3.connect('statistics.db')
c = db.cursor()

salary_by_year = pd.read_sql("SELECT strftime('%Y', published_at) as Year, ROUND(AVG(salary)) as avg_salary FROM vacancies WHERE salary is not null GROUP BY strftime('%Y', published_at)", db)
salary_by_year.to_csv('../static/tables/demand/salary_by_year.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(salary_by_year, '../static/plots/salary_by_year.png', 'Year', 'avg_salary')


count_by_year = pd.read_sql("SELECT strftime('%Y', published_at) as Year, COUNT(name) as count_vacancies FROM vacancies GROUP BY strftime('%Y', published_at)", db)
count_by_year.to_csv('../static/tables/demand/count_by_year.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(count_by_year, '../static/plots/count_by_year.png', 'Year', 'count_vacancies')


selected_salary_by_year = pd.read_sql(f"SELECT strftime('%Y', published_at) as Year, ROUND(AVG(salary)) as avg_salary_for_selected FROM vacancies WHERE salary is not null AND LOWER(name) LIKE '%{vacancy_name.lower()}%' GROUP BY strftime('%Y', published_at)", db)
selected_salary_by_year.to_csv('../static/tables/demand/selected_salary_by_year.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(selected_salary_by_year, '../static/plots/selected_salary_by_year.png', 'Year', 'avg_salary_for_selected')


selected_count_by_year = pd.read_sql(f"SELECT strftime('%Y', published_at) as Year, COUNT(name) as count_vacancies_for_selected FROM vacancies WHERE LOWER(name) LIKE '%{vacancy_name.lower()}%' GROUP BY strftime('%Y', published_at)", db)
selected_count_by_year.to_csv('../static/tables/demand/selected_count_by_year.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(selected_count_by_year, '../static/plots/selected_count_by_year.png', 'Year', 'count_vacancies_for_selected')


len_table = int(c.execute("SELECT COUNT(*) FROM vacancies WHERE salary is not null").fetchall()[0][0])

salary_by_area = pd.read_sql(f"SELECT area_name, ROUND(AVG(salary)) as avg_salary FROM vacancies WHERE salary is not null GROUP BY area_name HAVING COUNT(name) >= {len_table // 100} ORDER BY avg_salary DESC LIMIT 10", db)
salary_by_area.to_csv('../static/tables/geography/salary_by_area.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(salary_by_area, '../static/plots/salary_by_area.png', 'area_name', 'avg_salary')


fraction_by_area = pd.read_sql(f"SELECT area_name, ROUND(COUNT(salary) / {len_table}.0, 3) as fraction_vacancies FROM vacancies GROUP BY area_name HAVING COUNT(name) >= {len_table // 100} ORDER BY fraction_vacancies DESC LIMIT 10", db)
fraction_by_area.to_csv('../static/tables/geography/fraction_by_area.csv', encoding='utf-8-sig', index=False)
save_df_as_plot(fraction_by_area, '../static/plots/fraction_by_area.png', 'area_name', 'fraction_vacancies')

save_plots(salary_by_year, selected_salary_by_year, 'Year', 'avg_salary', 'avg_salary_for_selected', '../static/plots/diff_salary.png', ['средняя з/п в IT', 'средняя з/п для iOS-разработчиков'])
save_plots(count_by_year, selected_count_by_year, 'Year', 'count_vacancies', 'count_vacancies_for_selected', '../static/plots/diff_count.png', ['количество IT вакансий', 'количество вакансий iOS-разработчика'])

for year in range(2003, 2022):
    command = f'''
    WITH split(word, str) AS (
        SELECT '', key_skills||'\n' FROM vacancies WHERE LOWER(name) LIKE '%{vacancy_name.lower()}%' AND published_at like '{year}%' 
        UNION ALL
        SELECT
        substr(str, 0, instr(str, '\n')),
        substr(str, instr(str, '\n')+1)
        FROM split WHERE str!=''
    ) SELECT word as skill, COUNT(LOWER(word)) as count_skill FROM split WHERE word!='' GROUP BY LOWER(word) ORDER BY COUNT(LOWER(word)) DESC LIMIT 10;
    '''

    skills = pd.read_sql(command, db)
    if len(skills) == 0:
        continue
    skills.index += 1
    skills = skills.assign(year=lambda x: year)
    skills.to_csv(f'../static/tables/skills/skills-{year}.csv')
    save_df_as_plot(skills, f'../static/plots/skills/skills-{year}.png', 'skill', 'count_skill')
