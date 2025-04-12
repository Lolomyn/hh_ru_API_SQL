def get_companies_and_vacancies_count(vacancies: list):
    for vacancy in vacancies:
        company_name = vacancy[0]
        vacancy_name = vacancy[1]

        print(f"{company_name}: {vacancy_name}")


def get_all_vacancies(vacancies: list):
    for vacancy in vacancies:
        company_name = vacancy[0]
        vacancy_name = vacancy[1]
        min_salary = vacancy[2] if vacancy[2] else "Не указано"
        max_salary = vacancy[3] if vacancy[3] else "Не указано"
        currency = vacancy[4] if vacancy[4] else ""
        url = vacancy[5]

        print(f"Компания: {company_name}")
        print(f"Вакансия: {vacancy_name}")
        print(f"Зарплата: от {min_salary} до {max_salary} {currency}")
        print(f"Ссылка на вакансию: {url}\n")


def get_vacancies_with_higher_salary(vacancies: list):
    for vacancy in vacancies:
        company_name = vacancy[0]
        vacancy_name = vacancy[1]
        salary = vacancy[2] if vacancy[2] else "Не указано"
        currency = vacancy[3] if vacancy[4] else ""
        url = vacancy[4]

        print(f"Компания: {company_name}")
        print(f"Вакансия: {vacancy_name}")
        print(f"Зарплата: {salary} {currency}")
        print(f"Ссылка на вакансию: {url}\n")


def get_vacancies_with_keyword(vacancies: list):
    if vacancies:
        for vacancy in vacancies:
            print(vacancy)
    else:
        print("Вакансии по заданному ключевому слову не найдены...")
