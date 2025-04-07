# hh_ru_API_SQL
by lolomyn

## Install

### clone repo

    git clone git@github.com:Lolomyn/hh_ru_API_SQL.git

### install dependencies

    poetry add requests, psycopg2

### run

    python main.py

## Functional

### Class HeadHunterAPI
Класс для работы с API от HeadHunter: get-запрос к API

### Class DBManagerPostgres
Класс для работы с базами данных PostgreSQL

- **create_database / create_tables** - создать бд и таблиц
- **save_employers_to_db / save_vacancies_to_db** - сохранить данных в таблицы
- **get_companies_and_vacancies_count** - получить компании и количество вакансий у них
- **get_all_vacancies** - получить списка всех вакансий
- **get_avg_salary** - получить среднюю зарплату вакансий
- **get_vacancies_with_higher_salary** - получить вакансий с зарплатой выше среднего
- **get_vacancies_with_keyword** - получить вакансии по ключевому слову

